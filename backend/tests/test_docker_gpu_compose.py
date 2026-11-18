"""기본 설치는 CPU로 실행할 수 있고, GPU 예약은 추가 설정에서만 적용한다."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _backend_block(path: Path, *, has_frontend: bool) -> str:
    text = path.read_text(encoding="utf-8")
    block = text.split("\n  backend:\n", 1)[1]
    if has_frontend:
        block = block.split("\n  frontend:\n", 1)[0]
    return block


def test_default_compose_uses_auto_device_and_persistent_weights() -> None:
    compose = PROJECT_ROOT / "docker-compose.yml"
    backend = _backend_block(compose, has_frontend=True)

    assert "capabilities: [gpu]" not in backend
    assert "YOLO_DEVICE: ${YOLO_DEVICE:-}" in backend
    assert "YOLO_WEIGHTS_DIR: /app/models" in backend
    assert "- yolo_weights:/app/models" in backend


def test_gpu_override_reserves_device_without_forcing_cuda() -> None:
    override = PROJECT_ROOT / "docker-compose.gpu.yml"
    backend = _backend_block(override, has_frontend=False)

    assert backend.count("driver: nvidia") == 1
    assert "capabilities: [gpu]" in backend
    assert "YOLO_DEVICE" not in backend
    assert "volumes:" not in backend
