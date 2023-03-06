from integrations.anvyl import Anvyl
from integrations.shiphero import Shiphero


class ForgeIntegration(object):
    def __init__(self):
        # self.api_key = os.environ['API_KEY']
        self.anvyl_api_key = ""


    # Integration Anvyl
    def integrate_anvyl(self):
        anvyl = Anvyl()
        anvyl.run()

    # Integration Shiphero
    def integrate_shiphero(self):
        shiphero = Shiphero()
        shiphero.get_products()
        shiphero.create_kit()


def main(event, context):
    fi = ForgeIntegration()

    fi.integrate_anvyl()
    # fi.integrate_shiphero()


if __name__ == "__main__":
    main(0, 0)