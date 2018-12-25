def do_install(pkgs):
    try:
        # import pip
        try:
            from pip._internal import main
        except Exception:
            from pip import main
    except ImportError:
        error_no_pip()
    return main(['install'] + pkgs)


def do_uninstall(pkgs):
    try:
        # import pip
        try:
            from pip._internal import main
        except Exception:
            from pip import main
    except ImportError:
        error_no_pip()
    return main(['uninstall', '-y'] + pkgs)