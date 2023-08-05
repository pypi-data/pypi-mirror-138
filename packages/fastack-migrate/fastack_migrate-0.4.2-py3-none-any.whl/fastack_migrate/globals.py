from fastack.globals import state
from fastack.local import LocalProxy

from fastack_migrate import MigrateConfig


def _get_migrate_config() -> MigrateConfig:
    migrate = getattr(state, "migrate", None)
    if not isinstance(migrate, MigrateConfig):
        raise RuntimeError("fastack-migrate is not installed")
    return migrate


migrate: MigrateConfig = LocalProxy(_get_migrate_config)
