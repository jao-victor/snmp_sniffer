import asyncio
import ipaddress
import time

from icmplib import async_multiping

from pysnmp.hlapi.v3arch.asyncio import (
    SnmpEngine,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    get_cmd,
)


# -------- SNMP CHECK --------
async def check_snmp(ip, community, semaphore):
    async with semaphore:  # limita concorrência
        snmpEngine = SnmpEngine()

        try:
            errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
                snmpEngine,
                CommunityData(community, mpModel=1),  # SNMP v2c
                await UdpTransportTarget.create((ip, 161), timeout=2, retries=1),
                ContextData(),
                ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0")),
            )

            if errorIndication:
                return ip, False, "TIMEOUT/UNREACHABLE"

            if errorStatus:
                return ip, False, "AUTH/COMMUNITY ERROR"

            return ip, True, "OK"

        except Exception as e:
            return ip, False, f"ERROR: {e}"

        finally:
            snmpEngine.close_dispatcher()


# -------- MAIN --------
async def main():

    start_time = time.time()

    network = input("Digite a rede (ex: 192.168.1.0/24): ").strip()
    community = input("Digite a Community SNMP v2c: ").strip()

    address_range = ipaddress.ip_network(network)
    ip_list = [str(ip) for ip in address_range.hosts()]

    print("\nRealizando ping sweep...\n")

    devices = await async_multiping(ip_list, count=1, timeout=0.5)

    devices_up = [str(device.address) for device in devices if device.is_alive]

    print(f"{len(devices_up)} hosts ativos encontrados\n")

    if not devices_up:
        print("Nenhum host ativo.")
        return

    print("Iniciando verificação SNMP...\n")

    #  Limita concorrência para não abrir muitos sockets ao mesmo tempo
    semaphore = asyncio.Semaphore(100)

    tasks = [
        check_snmp(device, community, semaphore)
        for device in devices_up
    ]

    results = await asyncio.gather(*tasks)

    for ip, status, reason in results:
        if status:
            print(f"{ip} -> SNMP OK")
        else:
            print(f"{ip} -> SNMP FAIL ({reason})")

    end_time = time.time()
    print(f"\nTempo total: {round(end_time - start_time, 2)} segundos")


if __name__ == "__main__":
    asyncio.run(main())