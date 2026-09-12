import torch
import dataclasses

def get_device(verbose: bool = True) -> torch.device:
    """
    Auto-pick the best available device:
      - CUDA if available (NVIDIA GPU)
      - else MPS if available (Apple Silicon GPU)
      - else CPU
    """
    if torch.cuda.is_available():
        device = torch.device("cuda")
        name = torch.cuda.get_device_name(device)
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        device = torch.device("mps")
        name = "Apple MPS"
    else:
        device = torch.device("cpu")
        name = "CPU"

    if verbose:
        print(f"[PyTorch] Using device: {device} ({name})")
    return device

def broadcast_to_device(obj, device: torch.device):
    """Recursively move tensors or dict/list/tuple/dataclass of tensors to a device."""
    if torch.is_tensor(obj):
        return obj.to(device)
    elif isinstance(obj, dict):
        return {k: broadcast_to_device(v, device) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return type(obj)(broadcast_to_device(v, device) for v in obj)
    elif dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return type(obj)(**{f.name: broadcast_to_device(getattr(obj, f.name), device) for f in dataclasses.fields(obj)})
    else:
        return obj
