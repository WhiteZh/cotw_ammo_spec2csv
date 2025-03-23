from pathlib import Path
import csv
from dataclasses import dataclass, asdict
from xml.etree.ElementTree import ElementTree
from typing import Dict


@dataclass(init=True)
class Row:
    name: str
    max_range: float
    diameter: float
    length: float
    drag_coefficient: float
    kinetic_energy: float
    mass: float
    projectile_penetration: float
    projectile_damage: float
    projectile_expansion_rate: float
    projectile_contraction_rate: float
    projectile_max_expansion: float
    projectiles_per_shot: float
    ammunition_class: str

    def asdict(self) -> Dict:
        return asdict(self)


def xml_to_row(xml_file: Path) -> Row | None:
    try:
        et = ElementTree()
        root = et.parse(str(xml_file.resolve()))
        parent_layer = root.find('instances/instance')
        ammo_spec = parent_layer.find("member[@type='AmmunitionTuning']")
        ammo_class = parent_layer.find("member[@name='ammunition_class']")

        row = Row(
            name=xml_file.name[len("equipment_ammo_"):-len("_01.xml")],
            max_range=float(ammo_spec.find("member[@name='max_range']").text),
            diameter=float(ammo_spec.find("member[@name='diameter']").text),
            length=float(ammo_spec.find("member[@name='length']").text),
            drag_coefficient=float(ammo_spec.find("member[@name='drag_coefficient']").text),
            kinetic_energy=float(ammo_spec.find("member[@name='kinetic_energy']").text),
            mass=float(ammo_spec.find("member[@name='mass']").text),
            projectile_penetration=float(ammo_spec.find("member[@name='projectile_penetration']").text),
            projectile_damage=float(ammo_spec.find("member[@name='projectile_damage']").text),
            projectile_expansion_rate=float(ammo_spec.find("member[@name='projectile_expansion_rate']").text),
            projectile_contraction_rate=float(ammo_spec.find("member[@name='projectile_contraction_rate']").text),
            projectile_max_expansion=float(ammo_spec.find("member[@name='projectile_max_expansion']").text),
            projectiles_per_shot=float(ammo_spec.find("member[@name='projectiles_per_shot']").text),
            ammunition_class=','.join([str(child.find('member').text) for child in ammo_class]) if ammo_class is not None else ''
        )

        return row
    except Exception as e:
        print(f"`xml_to_row` failed for {xml_file}")
        print(e)
        print()
        return None


if __name__ == '__main__':
    xml_files = [file for file in Path(".").glob("**/*.xml") if isinstance(file, Path)]
    datas = [row.asdict() for file in xml_files if (row := xml_to_row(file)) is not None]
    with open('output.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'max_range', 'diameter', 'length',
                                               'drag_coefficient', 'kinetic_energy',
                                               'mass', 'projectile_penetration',
                                               'projectile_damage', 'projectile_expansion_rate',
                                               'projectile_contraction_rate', 'projectile_max_expansion',
                                               'projectiles_per_shot', 'ammunition_class'])
        writer.writeheader()
        writer.writerows(datas)