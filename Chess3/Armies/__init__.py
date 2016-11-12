import sys


if getattr(sys, 'frozen', False):
    # import all supported armies here for deployment build
    import Chess3.Armies.AnimalsImpl
    import Chess3.Armies.ClassicImpl
    import Chess3.Armies.ReaperImpl
    import Chess3.Armies.TwoKingsImpl
    import Chess3.Armies.EmpoweredImpl
    import Chess3.Armies.NemesisImpl
