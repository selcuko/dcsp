# Drone Controlling and Streaming Protocol (DCSP)


DCSP is a derived protocol out of TCP and powered by ZMQ. DCSP made to be easy to use for those custom drone controlling units.


## Features
  - Customizable telemetry data (Air-to-ground only for now)
  - Live broadcasting

> DCSP is actually a wrapper for ZMQ sockets, to make things more automated and more handled.

### Imports

* [pickle]
* [time]
* [zmq]

And of course Dillinger itself is open source with a [public repository][dill]
 on GitHub.

### Installation and Usage

```
pip install dcsp
```

**UAV:**
```
import dcsp

package = {
    "custom_telemetry_data" = "123"
}

uav = dcsp.UAV(port=333)
uav.wrap_frame(frame)
uav.package = package # identical to uav.wrap_package(custom_telemetry_data=123)
uav.send()
```

**Ground:**

```
import dcsp

gnd = dcsp.Ground()
gnd.connect(uav_ip_address, 333)
gnd.recv()

frame = gnd.frame
package = gnd.package
```

### Todos

 - (Ground-to-air) modifying UAV options

License
----

MIT



   [zmq]: https://zeromq.org/
   [pickle]: https://docs.python.org/3/library/pickle.html
   [time]: https://docs.python.org/3/library/time.html

