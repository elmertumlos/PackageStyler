def classFactory(iface):
    from .mainPlugin import PackageStyler
    return PackageStyler(iface)
