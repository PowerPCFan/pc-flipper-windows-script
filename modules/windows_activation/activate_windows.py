from modules.misc.enums import WindowsActivationMethod
import modules.windows_activation.massgrave as massgrave
import modules.windows_activation.product_key as product_key


def activate(method: WindowsActivationMethod, activation_key: str | None = None) -> None:
    """
    Activates Windows using the specified method
    """
    if method == WindowsActivationMethod.MASSGRAVE:
        massgrave.run()

    elif method == WindowsActivationMethod.ACTIVATION_KEY:
        if activation_key is not None:
            product_key.activate(key=activation_key)
        else:
            raise ValueError("Activation Key method was specified but an activation key was not provided.")

    else:
        raise ValueError("Invalid activation method specified.")
