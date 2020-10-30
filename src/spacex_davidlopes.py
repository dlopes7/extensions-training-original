import requests
from ruxit.api.base_plugin import RemoteBasePlugin


class SpaceXExtension(RemoteBasePlugin):

    def query(self, **kwargs):
        # Obter a lista de navios
        ships = self.get_ships()

        # Criar os Groups
        # Obtem os nomes unicos dos tipos de navios
        ship_types = set([ship["ship_type"] for ship in ships])

        groups = {}
        for ship_type in ship_types:
            group_name = f"{ship_type} David Lopes"
            groups[ship_type] = self.topology_builder.create_group(group_name, group_name)

        for ship in ships:
            self.logger.info(f"Processing ship {ship['ship_name']}")

            # Obtém o grupo para esse navio
            group = groups[ship["ship_type"]]

            # Cria o Custom Device
            ship_id = f"{ship['ship_id']} David Lopes"
            ship_name = f"{ship['ship_name']} David Lopes"
            device = group.create_device(ship_id, ship_name)

            # Envia uma métrica absoluta
            device.absolute("fuel", ship["fuel"])

            for engine in ship["thrust"]:
                device.absolute(key="thrust", value=engine["power"], dimensions={"Engine": engine["engine"]})

            device.add_endpoint(ship["ship_ip"])

            device.report_property("Home port", ship.get("home_port", ""))
            device.report_property("Roles", ",".join(ship.get("roles", [])))

        # Criar os Custom Devices
        # Enviar a métrica Combustivel

        pass

    def get_ships(self):
        return requests.get("http://ec2-3-235-75-78.compute-1.amazonaws.com/v3/ships").json()

