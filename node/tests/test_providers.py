import itertools

from conftest import FlatpakBuilder, ProviderFactorySpec
from flatpak_node_generator.manifest import ManifestGenerator


async def test_special_electron(
    flatpak_builder: FlatpakBuilder,
    provider_factory_spec: ProviderFactorySpec,
) -> None:
    with ManifestGenerator() as gen:
        await provider_factory_spec.generate_modules('electron', gen)

    flatpak_builder.build(
        sources=itertools.chain(gen.ordered_sources()),
        commands=[provider_factory_spec.install_command],
        use_node=True,
    )

    electron_version = (
        flatpak_builder.module_dir / 'node_modules' / 'electron' / 'dist' / 'version'
    )
    assert electron_version.read_text() == '18.2.0'