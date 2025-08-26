from typing import Literal, cast

GpiSignal = Literal['HIGH', 'LOW']

GPI_SIGNAL_VALUES: set[GpiSignal] = { 'HIGH', 'LOW',  }

def check_gpi_signal(value: str) -> GpiSignal:
    if value in GPI_SIGNAL_VALUES:
        return cast(GpiSignal, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GPI_SIGNAL_VALUES!r}")
