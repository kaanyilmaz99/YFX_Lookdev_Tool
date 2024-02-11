# STYLE ***************************************************************************
# content  = assignment
#
# date     = 2024-09-02
# email    = contact@alexanderrichtertd.com
# modified = Kaan Yilmaz
#************************************************************************************

# original: logging.init.py

def findCaller(self):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.

    On some versions of IronPython, currentframe() returns None if
    IronPython isn't run with -X:Frames.
    """

    frame_number = currentframe()
    if frame_number:
        frame_number = frame_number.f_back

    while hasattr(frame_number, "f_code"):
        frame_code = frame_number.f_code
        file_name = os.path.normcase(frame_co.co_filename)

        if file_name == _srcfile:
            frame_number = frame_number.f_back
            rv = "(unknown file)", 0, "(unknown function)"
        else:
            rv = (frame_code.co_filename, frame_number.f_lineno, frame_code.co_name)

    return rv
