# A/D Defense Tooling

The following is an overview of defense tooling for A/D CTFs.

Customizable proxies are great for quickly adding attack patterns
to block existing exploits. Since an opponent tooling can't distinguish
a good from a bad patch, they
will [typically](localhost:8000/attack-defense/playing/strategy/#attack-vs-defense)
not waste time changing the behavior of their exploit script for a specific target.

##  OpenAttackDefenseTools/yampa

[YAMPA](https://github.com/OpenAttackDefenseTools/yampa)
is "**Y**et **A**nother **M**itM **P**roxy for use in **A**/D CTFs" and allows
manipulating traffic between the game network and the vulnbox.

It can be customized via python plugins that implement hooks for *decrypting*,
*filtering*, *logging* and re-*encrypting* to manipulate traffic. This
architecture allows plugins to implement a *decryption* step which when
successful can be utilized by a different plugin that does *logging* and
*filtering*.

*[MitM]: Man in the Middle

## ByteLeMany/ctf_proxy

[ctf_proxy](https://github.com/ByteLeMani/ctf_proxy) is a TCP/HTTP(s) proxy
that allows manipulating traffic with custom python filters, which auto-reload
on edit.

The filter interface receives a single `TCPStream` or `HTTPStream` object depending
on the traffic type configured. This stream allows accessing previous packets
sent in the session, viewing reassembled traffic and filtering
or blocking the connection based on this information.
