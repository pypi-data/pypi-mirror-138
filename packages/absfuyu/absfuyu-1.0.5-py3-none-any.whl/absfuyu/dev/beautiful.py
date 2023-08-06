"""
Make output more beautiful
"""


# Library
##############################################################
from functools import wraps as __wraps
from time import perf_counter as __perf

BEAUTIFUL_MODE = False

try:
    # from rich import print
    from rich.align import Align as __Align
    from rich.console import Console as __Console
    from rich.console import Group as __Group
    from rich.panel import Panel as __Panel
    from rich.table import Table as __Table
    from rich.text import Text as __Text
except:
    print("This feature is in absfuyu[beautiful] package")
else:
    BEAUTIFUL_MODE = True



# Function
##############################################################
def beautiful_output(layout_option: int = 3):
    """
    Beautify function output
    """
    
    if BEAUTIFUL_MODE:
        def decorator(func):

            @__wraps(func)
            def wrapper(*args, **kwargs):
                
                # Measure performance
                start_time = __perf()
                f = func(*args, **kwargs)
                finished_time = __perf()
                elapsed = f"Time elapsed: {finished_time - start_time:,.6f} s"
                
                # Make header
                header_table = __Table.grid(expand=True)
                header_table.add_row(
                    __Panel(
                        __Align(f"[b]Function: {func.__name__}", align="center"),
                        style="white on blue",
                    ),
                )

                # Make footer
                footer_table = __Table.grid(expand=True)
                footer_table.add_row(
                    __Panel(
                        __Align("[b]END PROGRAM", align="center"),
                        style="white on blue",
                    ),
                )
                
                # Make output table
                out_table = __Table.grid(expand=True)
                out_table.add_column(ratio=2) # result
                out_table.add_column() # performance
                r_txt = __Text(
                    str(f),
                    overflow="fold",
                    no_wrap=False,
                    tab_size=2,
                )
                result_panel = __Panel(
                    __Align(r_txt, align="center"),
                    title="[bold]Result[/]",
                    border_style="green",
                    highlight=True,
                )
                performance_panel = __Panel(
                    __Align(elapsed, align="center"),
                    title="[bold]Performance[/]",
                    border_style="red",
                    highlight=True,
                    height=result_panel.height,
                )
                out_table.add_row(
                    result_panel,
                    performance_panel,
                )

                # Make a blue line for no reason
                line = __Table.grid(expand=True)
                line.add_row(__Text(style="white on blue"))

                # Make layout
                layout = {
                    1: __Group(header_table, out_table, footer_table),
                    2: __Group(header_table, result_panel, performance_panel, footer_table),
                    3: __Group(header_table, result_panel, performance_panel, line),
                }
                if layout_option in layout:
                    return layout[layout_option]
                else:
                    return layout[3]
                # return layout[3]

            return wrapper
        
        return decorator

    else:
        return None


# rich's console.print wrapper
print = __Console().print


# # test
# code="""\
# def lmao(x):
#   for _ in range(100):
#     print(x)
#   return None"""


# @beautiful_output()
# def demo(x):
#     return x


# from rich.console import Console
# console = Console()
# console.print(demo(code))