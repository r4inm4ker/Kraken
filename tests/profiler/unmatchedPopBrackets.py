from kraken.core.profiler import Profiler
import time
import json

profiler = Profiler()
time.sleep(0.15)
profiler.push('fn1')
time.sleep(0.05)
profiler.push('fn2')
time.sleep(0.01)
profiler.pop()
profiler.generateReport()
