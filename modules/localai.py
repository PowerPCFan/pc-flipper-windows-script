import zipfile
import pathlib
import subprocess
import time
import atexit
import sys
import requests
from weakref import WeakSet
from openai import OpenAI
from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMessageBox,
    QPushButton, QTextEdit, QVBoxLayout,
    QWidget
)
from modules.color.ansi_codes import RED, RESET, CYAN, GREEN
import modules.misc.global_vars as gv
from modules.misc.utils import download_large_file


_ACTIVE_LOCALAI: WeakSet["LocalAI"] = WeakSet()
_AI_DESCRIPTION_WINDOW: "AIDescriptionGeneratorWindow | None" = None


def close_all_localai() -> None:
    for instance in list(_ACTIVE_LOCALAI):
        try:
            instance.close()
        except Exception:
            pass


class LocalAI:
    def __init__(self) -> None:
        # self.dir = gv.SCRIPT_TEMP_PATH / "localai"
        self.dir = pathlib.Path("C:/Users/Charlie/deletethis/localai")
        self.dir.mkdir(parents=True, exist_ok=True)

        self.gguf = self.dir / "llama-3.2-3b-instruct-q4_k_m.gguf"
        self.zip = self.dir / "llamacpp.zip"
        self.unzipped = self.dir / "llamacpp"

        self.llama_server = self.unzipped / "llama-server.exe"
        self.server_host = "127.0.0.1"
        self.server_port = 8080
        self.server_url = f"http://{self.server_host}:{self.server_port}"
        self.openai_client = OpenAI(
            base_url=f"{self.server_url}/v1",
            api_key="local"
        )
        self.temperature = 0.5
        self.top_p = 0.5
        self.frequency_penalty = 0.2
        self.model_name: str | None = None
        self.server_process: subprocess.Popen | None = None
        self._owns_server_process = False
        _ACTIVE_LOCALAI.add(self)
        atexit.register(self.close)

    def download_model(self) -> bool:
        gguf_success = False
        zip_success = False

        if not self.gguf.exists():
            print(f"{CYAN}Downloading Llama 3.2 3B Instruct model...{RESET}")

            url = "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf"  # noqa: E501
            gguf_success = download_large_file(
                url=url,
                destination=str(self.gguf.resolve()),
                timeout=10
            )

            if gguf_success:
                print(f"{GREEN}Model downloaded successfully.{RESET}")
            else:
                print(f"{RED}Error: Model download failed.{RESET}")
        else:
            gguf_success = True
            print(f"{GREEN}Model already exists. Skipping download.{RESET}")

        if not self.zip.exists():
            url = "https://github.com/ggml-org/llama.cpp/releases/download/b8252/llama-b8252-bin-win-cpu-x64.zip"
            zip_success = download_large_file(
                url=url,
                destination=str(self.zip.resolve()),
                timeout=10
            )

            if zip_success:
                print(f"{GREEN}llama.cpp binary downloaded successfully. Unzipping...{RESET}")

                try:
                    with zipfile.ZipFile(self.zip) as z:
                        z.extractall(self.unzipped)
                except Exception:
                    print(f"{RED}Error: Failed to unzip llama.cpp binary.{RESET}")
                    zip_success = False

                if self.llama_server.exists():
                    print(f"{GREEN}llama.cpp is ready to use.{RESET}")
                else:
                    print(f"{RED}Error: llama.cpp binary not found after unzipping.{RESET}")
                    zip_success = False
            else:
                print(f"{RED}Error: llama.cpp binary download failed.{RESET}")
        else:
            zip_success = True
            print(f"{GREEN}llama.cpp binary already exists. Skipping download and unzip.{RESET}")

        return (gguf_success and zip_success)

    def create_prompt(
        self,
        cpu: str | None = None,
        ram: str | None = None,
        board: str | None = None,
        storage: str | None = None,
        gpu: str | None = None,
        os: str | None = None,
        additional_details: str | None = None
    ) -> str:
        components_string = "; ".join([f"{v}: {val}" for k, v in {
            "cpu": "CPU", "ram": "RAM", "board": "Motherboard",
            "storage": "Storage", "gpu": "GPU", "os": "Operating System"
        }.items() if (val := locals().get(k)) is not None])

        additional_details_block = (
            f"Additional listing details to include when relevant:\n{additional_details.strip()}\n"
            if additional_details and additional_details.strip()
            else ""
        )

        return (
            "Generate an eBay-style listing description for a PC using the provided specs and details.\n\n"
            f"PC specs:\n{components_string}\n\n"
            f"{additional_details_block}"
        )

    # def _get_system_instructions(self) -> str:
    #     return (
    #         "You are a professional copywriter specializing in product descriptions. "
    #         "Write persuasive, grounded eBay-style listings for prebuilt PCs. "
    #         "Aim for high-quality writing without generic filler.\n\n"
    #         "Rules:\n"
    #         "- Output plain Markdown only. Start directly with listing content.\n"
    #         "- Keep tone natural, seller-like, and specific to provided details.\n"
    #         "- Use persuasive selling language with a medium balance: confident and appealing, but not overhyped for what it actually is.\n"  # noqa: E501
    #         "- Avoid extreme hype words like 'unparalleled', 'ultimate', 'best-in-class', 'game-changing', 'unbeatable', 'insane performance', or 'the best on the market' unless explicitly supported. Prefer moderate phrasing like 'good performance', 'well-suited for', 'great for', 'solid choice', and 'reliable'.\n"  # noqa: E501
    #         "- Aim for this structure: opening sentences (3-5 sentences) with selling points based on the components, "  # noqa: E501
    #         "'PC Specs' bullets, then extra sections that make sense based on all provided data.\n"
    #         "- Section names can be flexible; prefer user-provided section names when available.\n"
    #         "- Only include claims supported by provided details or safe high-level usage inferences.\n"
    #         "- Do not invent exact numbers, benchmark data, compatibility caveats, or market-position claims unless explicitly provided.\n"  # noqa: E501
    #         "- Do not infer exact hardware stats unless explicitly provided (e.g. cores, threads, cache, clock speeds, wattage, and more).\n"  # noqa: E501
    #         "- Never invent policy/business details. If shipping/returns/warranty/condition/support terms are not explicitly provided, omit those sections entirely.\n"  # noqa: E501
    #         "- Do not use recency/superlative claims like 'latest', 'newest', or similar ranking language unless explicitly supported by provided details.\n"  # noqa: E501
    #         "- Do not invent named/internal testing sources (for example "
    #         "'our proprietary testing') unless explicitly provided.\n"
    #         "- Section gate: if a section cannot be written strictly from provided facts, omit that section.\n"
    #         "- 'PC Specs' must list provided hardware/spec fields only.\n"
    #         "- If benchmark/FPS details are provided, include them in a benchmark/performance section using a bullet list format.\n"  # noqa: E501
    #         "- Always include a 'What's in the Box?' section. It must contain at least 'Full PC' plus any additional explicitly provided physical in-box items. Do not add things that you think should be there, only add 'Full PC' and anything else the user explicitly said comes with the PC. (Physical items only, like a power cable, not software/drivers)\n"  # noqa: E501
    #         "- Do not place software/setup facts in 'What's in the Box?' (for example drivers, activation status, OpenRGB, installed apps). Put those only in a setup/software section.\n"  # noqa: E501
    #         "- Do not add sections that only restate PC Specs in sentence form. Create extra sections only when they add new, provided information.\n"  # noqa: E501
    #         "- Never create synthetic sections like System Requirements, Warranty, Support, Shipping, Returns, or Condition unless those details were explicitly provided.\n"  # noqa: E501
    #         "- Keep internal consistency and avoid contradictions.\n"
    #         "- Omit unsupported sections instead of filling with assumptions. Even if you think a section should be there, omit it instead of using placeholders, unless real information was provided.\n"  # noqa: E501
    #         "- Target around 450 words, however, shorter is acceptable when input is limited, and longer is acceptable with extensive input.\n"  # noqa: E501
    #     )

    def _get_system_instructions(self) -> str:
        return """\
You are a professional PC hardware copywriter. Your task is to transform technical data into an eBay listing using a specific 4-part structure.

STRUCTURE PROTOCOL:
1. **The Hook**: 3-5 persuasive sentences highlighting the CPU and GPU combination. Use "grounded" language (e.g., "solid choice," "reliable performance").
2. **PC Specs**: A bulleted list of provided hardware ONLY.
3. **Extra Details**: Create separate sections (e.g., "Performance," "Software") ONLY if the user provides data for them.
4. **What's in the Box?**: A bulleted list of PHYSICAL items only (Full PC, cables, etc.).

STRICT CONSTRAINTS:
- Use plain Markdown. Additionally, you can sparingly use emojis for extra flair, but avoid overuse.
- No "marketing fluff" like "ultimate" or "insane."
- Include only claims supported by provided specs/details.
- Do not infer or invent exact technical details unless explicitly provided (for example cores, clocks, benchmark values, timelines, or compatibility caveats).
- Do not claim market position or recency (for example latest/newest/current-gen) unless explicitly provided.
- Never mention things such as Warranty, Shipping, Returns, or Technical Support unless explicitly provided.
- Software and Setup info (Windows, OpenRGB, Drivers) must NEVER be in 'What's in the Box?'. Put them in a 'Software' section.
- If data is not provided, do not create a section for it.
- Target around 500 words when enough details are provided. Use shorter output when input is limited.
"""  # noqa: E501

    def ask(self, prompt: str) -> str:
        if not self._ensure_server_running():
            return ""

        try:
            model_name = self._get_model_name()
            if not model_name:
                print(f"{RED}Error: no model available from llama-server OpenAI API.{RESET}")
                return ""

            response = self.openai_client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": self._get_system_instructions()},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                max_tokens=1750
            )
        except Exception as exc:
            print(f"{RED}Error: OpenAI client request to llama-server failed: {exc}{RESET}")
            return ""

        output_text = ""
        if response.choices and response.choices[0].message:
            output_text = (response.choices[0].message.content or "").strip()

        if not output_text:
            print(f"{RED}Error: llama-server returned an empty completion.{RESET}")
            return ""

        return output_text

    def _get_model_name(self) -> str | None:
        if self.model_name:
            return self.model_name

        try:
            models = self.openai_client.models.list()
            if models.data:
                self.model_name = models.data[0].id
        except Exception:
            self.model_name = None

        return self.model_name

    def _ensure_server_running(self) -> bool:
        if self._is_server_healthy():
            return True

        if not self.llama_server.exists():
            print(f"{RED}Error: llama-server binary not found. Run download_model() first.{RESET}")
            return False

        if not self.gguf.exists():
            print(f"{RED}Error: model file not found. Run download_model() first.{RESET}")
            return False

        cmd = [
            str(self.llama_server.resolve()),
            "--model", str(self.gguf.resolve()),
            "--host", self.server_host,
            "--port", str(self.server_port),
            "--ctx-size", "4096"
        ]

        try:
            self.server_process = subprocess.Popen(
                cmd,
                # stdout=subprocess.DEVNULL,
                # stderr=subprocess.DEVNULL,
                # print stdout and stderr to console for debugging
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self._owns_server_process = True
        except OSError as exc:
            print(f"{RED}Error: failed to start llama-server: {exc}{RESET}")
            return False

        for _ in range(30):
            if self._is_server_healthy():
                return True

            if self.server_process.poll() is not None:
                print(f"{RED}Error: llama-server exited unexpectedly while starting.{RESET}")
                return False

            time.sleep(1)

        print(f"{RED}Error: timed out waiting for llama-server to start.{RESET}")
        return False

    def _is_server_healthy(self) -> bool:
        for endpoint in ("/health", "/props"):
            try:
                response = requests.get(f"{self.server_url}{endpoint}", timeout=2)
                if response.ok:
                    return True
            except requests.exceptions.RequestException:
                continue

        return False

    def close(self) -> None:
        if not self._owns_server_process or not self.server_process:
            return

        if self.server_process.poll() is not None:
            return

        try:
            self.server_process.terminate()
            self.server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.server_process.kill()
            self.server_process.wait(timeout=2)
        except Exception:
            pass

    def __del__(self) -> None:
        # Destructor timing isn't guaranteed, but this helps in REPL/manual tests.
        try:
            self.close()
        except Exception:
            pass


class AIDescriptionGeneratorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ai = LocalAI()
        self.spec_inputs: dict[str, QLineEdit] = {}
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("AI Description Generator")
        self.resize(900, 760)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        title = QLabel("AI Description Generator")
        title.setStyleSheet("font-size: 20px; font-weight: 600;")
        layout.addWidget(title)

        subtitle = QLabel("Review detected specs, add details, and generate a listing description.")
        subtitle.setStyleSheet("color: #666;")
        layout.addWidget(subtitle)

        self._add_spec_inputs(layout)

        details_label = QLabel("Extra Details")
        details_label.setStyleSheet("font-weight: 600;")
        layout.addWidget(details_label)

        self.extra_details = QTextEdit()
        self.extra_details.setPlaceholderText(
            "Example: Includes power cable and quick start guide; drivers preinstalled and Windows activated; "
            "uses OpenRGB; 400 FPS in Minecraft and 200 FPS in Fortnite (1080p medium settings)"
        )
        self.extra_details.setFixedHeight(110)
        layout.addWidget(self.extra_details)

        controls = QHBoxLayout()
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self._on_generate_clicked)
        controls.addWidget(self.generate_button)
        controls.addStretch()
        layout.addLayout(controls)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #444;")
        layout.addWidget(self.status_label)

        output_label = QLabel("Generated Description")
        output_label.setStyleSheet("font-weight: 600;")
        layout.addWidget(output_label)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setMinimumHeight(260)
        layout.addWidget(self.output_box)

        self.copy_description_button = QPushButton("Copy Description")
        self.copy_description_button.setEnabled(False)
        self.copy_description_button.clicked.connect(self._copy_description)
        layout.addWidget(self.copy_description_button)

    def _add_spec_inputs(self, layout: QVBoxLayout):
        defaults = {
            "cpu": gv.CPU,
            "ram": gv.RAM,
            "board": gv.FULL_MOTHERBOARD_NAME,
            "storage": gv.STORAGE,
            "gpu": gv.GPU,
            "os": gv.WINDOWS_OS_VERSION,
        }

        for key, label in (
            ("cpu", "CPU"),
            ("ram", "RAM"),
            ("board", "Motherboard"),
            ("storage", "Storage"),
            ("gpu", "GPU"),
            ("os", "Operating System"),
        ):
            row = QHBoxLayout()
            row_label = QLabel(label)
            row_label.setFixedWidth(130)
            row_input = QLineEdit(defaults.get(key, ""))
            self.spec_inputs[key] = row_input
            row.addWidget(row_label)
            row.addWidget(row_input)
            layout.addLayout(row)

    def _on_generate_clicked(self):
        self.generate_button.setEnabled(False)
        self.status_label.setText("Generating description...")
        QApplication.processEvents()

        try:
            prompt = self.ai.create_prompt(
                cpu=self.spec_inputs["cpu"].text().strip() or None,
                ram=self.spec_inputs["ram"].text().strip() or None,
                board=self.spec_inputs["board"].text().strip() or None,
                storage=self.spec_inputs["storage"].text().strip() or None,
                gpu=self.spec_inputs["gpu"].text().strip() or None,
                os=self.spec_inputs["os"].text().strip() or None,
                additional_details=self.extra_details.toPlainText().strip() or None,
            )

            description = self.ai.ask(prompt)
            if not description:
                self.status_label.setText("Generation failed.")
                QMessageBox.warning(self, "Generation Failed", "The AI returned an empty description.")
                return

            self.output_box.setPlainText(description)
            self.copy_description_button.setEnabled(True)
            self.status_label.setText("Generated successfully.")
        finally:
            self.generate_button.setEnabled(True)

    def _copy_description(self):
        description = self.output_box.toPlainText().strip()
        if not description:
            return
        clipboard = QApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(description)
        self.status_label.setText("Description copied to clipboard.")

    def closeEvent(self, a0):
        self.ai.close()
        super().closeEvent(a0)


def show_ai_description_generator_window() -> None:
    global _AI_DESCRIPTION_WINDOW

    app = QApplication.instance()
    owns_app = app is None
    if owns_app:
        app = QApplication(sys.argv)

    _AI_DESCRIPTION_WINDOW = AIDescriptionGeneratorWindow()
    _AI_DESCRIPTION_WINDOW.show()

    if owns_app:
        app.exec()

# example usage
# from modules.localai import LocalAI; ai = LocalAI(); ai.download_model(); ai.ask(ai.create_prompt(
#     cpu="AMD Ryzen 5 3600",
#     ram="16GB DDR4 3600MHz",
#     board="ASRock B450M AC R2.0",
#     storage="512GB NVMe SSD (PCIe Gen 4)",
#     gpu="Nvidia GeForce RTX 5060",
#     os="Windows 11 Pro 24H2",
#     additional_details=(
#         "Includes power cable and quick start guide; "
#         "drivers preinstalled and Windows activated; "
#         "uses OpenRGB; "
#         "400 FPS in Minecraft and 200 FPS in Fortnite (all games tested at 1080p medium settings)"
#     )
# ))
