**NAME**

 **GENOCIDE** to reconsider OTP-CR-117/19

**SYNOPSIS**

 ``genocidectl <cmd> [key=value] [key==value]``

**DESCRIPTION**

 **GENOCIDE** is a python3 program that holds evidence that the king of the
 netherlands is doing a genocide, a written response where the king of
 the netherlands confirmed taking note of “what i have written”, namely
 proof that medicine he uses in treatement laws like zyprexa, haldol,
 abilify and clozapine are poison that makes impotent, is both physical
 (contracted muscles) and mental (let people hallucinate) torture and kills
 members of the victim groups, namely elderly and handicapped (Wzd), mentally
 disturbed (WvGGZ) and criminals (Wfz).

 **GENOCIDE** contains correspondence with the International Criminal Court,
 asking for arrest of the king of the netherlands, for the genocide he is
 committing with his new treatement laws. Current status is an outside the
 jurisdiction judgement of the prosecutor which requires a reconsider to
 have the king actually arrested.

 **GENOCIDE** is also an IRC bot that can run as a background daemon for 24/7
 day presence in an IRC channel, act as a UDP to IRC gateway and is a 
 programmable bot that you can program your commands for.

 @IntlCrimCourt @KarimKhanQC reconsider OTP-CR-117/19, after 2002, as article 6, 
 other groups than mentioned, article 15 request. http://genocide.rtfd.io #ggz

**INSTALL**

 ``pip3 install genocide``

**CONFIGURATION**

 | ``cp /usr/local/share/genocide/genocide.service /etc/systemd/system``
 | ``systemctl enable genocide --now``

 **irc**

 | ``genocidectl cfg server=<server> channel=<channel>``
 | ``genocidectl cfg nick=<nick>``

 default channel/server is #genocide on localhost

 **sasl**

 | ``genocidectl pwd <nickservnick> <nickservpass>``
 | ``genocidectl cfg password=<outputfrompwd>``

 **users**

 | ``genocidectl cfg users=True``
 | ``genocidectl met <userhost>``

**CODE**

 code can be found at https://github.com/bthate/genocide

**COPYRIGHT**

 ``genocide`` is placed in the Public Domain, no Copyright, no LICENSE.

**AUTHOR**

 Bart Thate 
