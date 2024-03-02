from configparser import ConfigParser
from dataclasses import dataclass


@dataclass
class DataConfig:
    data_file_name: str


@dataclass
class WindowConfig:
    title: str
    width: int
    height: int


@dataclass
class SceneConfig:
    width: int
    height: int
    grid_size: int


@dataclass
class Config:
    data: DataConfig
    window: WindowConfig
    scene: SceneConfig


def load_config(file_name: str) -> Config:
    config = ConfigParser()
    config.read(file_name)

    data = config['data']
    window = config['window']
    scene = config['scene']

    return Config(
        data=DataConfig(
            data_file_name=data.get('data_file_name'),
        ),
        window=WindowConfig(
            title=window.get('title'),
            width=window.getint('width'),
            height=window.getint('height'),
        ),
        scene=SceneConfig(
            width=scene.getint('width'),
            height=scene.getint('height'),
            grid_size=scene.getint('grid_size')
        )
    )
