import time
from modules.localai import LocalAI

ai = LocalAI()

print("=" * 31 + "\nLatest Version Tests - 10x Runs\n" + "=" * 31 + "\n\n")

outputs: list[str] = []

for idx in range(10):
    print(f"Run {idx + 1} started!")

    start = time.time()

    output = ai.ask(ai.create_prompt(
        cpu="AMD Ryzen 5 3600",
        ram="16GB DDR4 3600MHz",
        board="ASRock B450M AC R2.0",
        storage="512GB NVMe SSD (PCIe Gen 4)",
        gpu="Nvidia GeForce RTX 5060",
        os="Windows 11 Pro 24H2",
        additional_details=(
            "Includes power cable and quick start guide; "
            "drivers preinstalled and Windows activated; "
            "uses OpenRGB; "
            "400 FPS in Minecraft and 200 FPS in Fortnite (all games tested at 1080p medium settings)"
        )
    ))

    end = time.time()

    outputs.append(output)
    print(f"Run {idx + 1} complete. Elapsed: {end - start:.2f}s\n\n")

print("All runs completed!")

for index, output in enumerate(outputs):
    print(f"\n\nOutput from Run {index + 1}:\n" + "-" * 20)
    print("\n".join([f"    {line}" for line in output.splitlines()]))
