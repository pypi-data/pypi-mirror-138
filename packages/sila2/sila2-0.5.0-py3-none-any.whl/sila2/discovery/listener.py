import itertools
import warnings
from typing import Dict, Optional
from uuid import UUID

from cryptography import x509
from zeroconf import ServiceBrowser, ServiceInfo, ServiceListener, Zeroconf

from sila2.client.sila_client import SilaClient


class SilaServiceListener(ServiceListener):
    parent_browser: ServiceBrowser
    services: Dict[str, SilaClient]

    def __init__(
        self,
        parent_browser: ServiceBrowser,
        *,
        insecure: bool = False,
        root_certs: Optional[bytes] = None,
        private_key: Optional[bytes] = None,
        cert_chain: Optional[bytes] = None,
    ):
        self.parent_browser = parent_browser
        self.services = {}
        self.insecure = insecure
        self.root_certs = root_certs
        self.private_key = private_key
        self.cert_chain = cert_chain

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        self.__add_client(info)

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        self.__add_client(info)

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        if name in self.services:
            self.services.pop(name)

    def __add_client(self, service_info: Optional[ServiceInfo] = None) -> None:
        if service_info is None:  # happens sometimes
            return

        service_name = service_info.name
        ip_address = service_info.parsed_addresses()[0]

        try:
            ca = self.__get_ca_from_service_info(service_info)

            if ca is not None:
                self.services[service_name] = SilaClient(ip_address, service_info.port, root_certs=ca)
            elif any(par is not None for par in (self.cert_chain, self.private_key, self.root_certs)):
                self.services[service_name] = SilaClient(
                    ip_address,
                    service_info.port,
                    cert_chain=self.cert_chain,
                    private_key=self.private_key,
                    root_certs=self.root_certs,
                )
            elif self.insecure:
                self.services[service_name] = SilaClient(ip_address, service_info.port, insecure=True)
            else:
                raise RuntimeError("Ignored unencrypted server")
        except Exception as ex:
            service_uuid = UUID(service_name.split(".")[0])
            warnings.warn(
                RuntimeWarning(
                    f"SiLA Server Discovery found a service with UUID {service_uuid} but failed to connect to it: "
                    f"{ex.__class__.__name__} - {ex}"
                )
            )

    @staticmethod
    def __get_ca_from_service_info(service_info: ServiceInfo) -> Optional[bytes]:
        if b"ca0" not in service_info.properties:
            return None

        ca = b""
        for i in itertools.count():
            key = f"ca{i}".encode("ascii")
            if key in service_info.properties:
                ca += service_info.properties[key]
            else:
                break
        if ca == b"":
            return
        x509.load_pem_x509_certificate(ca)  # check if a full CA was found
        return ca
