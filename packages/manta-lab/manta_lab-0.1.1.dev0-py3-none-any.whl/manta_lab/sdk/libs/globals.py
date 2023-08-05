import manta_lab as ml


def set_globals(
    # global vars
    run=None,
    config=None,
    meta=None,
    summary=None,
    # global function
    log=None,
    save=None,
    alarm=None,
    use_artifact=None,
    log_artifact=None,
):
    kwargs = locals()
    for k, v in kwargs.items():
        if v:
            setattr(mc, k, v)


def unset_globals():
    ml.run = None
    ml.config = None
    ml.meta = None
    ml.summary = None
    ml.log = None
    ml.save = None
    ml.alarm = None
    ml.use_artifact = None
    ml.log_artifact = None
