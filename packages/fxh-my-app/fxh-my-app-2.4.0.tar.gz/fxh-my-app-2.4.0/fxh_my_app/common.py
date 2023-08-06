def get_contract_type(type_name: str) -> int:
    # 0=unknown:未知
    # 1=spot:现货
    # 2=swap:永续合约
    # 3=cw:当周连续合约
    # 4=nw:下周连续合约
    # 5=cq:当季连续合约
    # 6=nq:下季连续合约

    if type_name is None:
        return 0

    if len(type_name) == 0:
        return 0

    name = type_name.strip().lower()

    if name == 'spot':
        return 1

    if name == 'swap':
        return 2

    if name == 'cw':
        return 3

    if name == 'nw':
        return 4

    if name == 'cq':
        return 5

    if name == 'nq':
        return 6

    return 0
