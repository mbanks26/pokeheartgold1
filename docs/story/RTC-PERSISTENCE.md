# Persistent story flags across calendar changes

The recovered prototype reserved B5E/B5F for companion status. Story development
also used B50-B57 and B5D. These previously unused bits lie at the tail of the
native AA0-B5F daily-reset range. Battery saves retained them until a daily reset,
which could erase story progress or turn a deliberately disabled companion on
again through the legacy starter fallback. Same-day save/load tests missed this.

ClearDailyFlags now preserves B50-B57 and B5D-B5F while clearing all other original
daily bits, including unused B58-B5C. Save structures, offsets and flag IDs remain
unchanged. Existing saved status transfers directly. New Bark additionally uses
its persistent scene variable to restore the hidden introduction actors if an
older build already cleared their flag.

The actual reset function passes 8,192 sanitized host cases, preserving joined,
deactivated and female-route status while ordinary daily flags reset. A DeSmuME
authored battery-save fixture forces the native elapsed-day callback: unused daily
sentinel B49 clears, sister Eevee B51 and joined B5F remain set, and exactly one
Sabrina and one native Pokemon follow. The tested integrated ROM SHA-1 is
c794f957edb5656e7298b50548afcaf4a5497c25; its additional partner changes are being
validated separately. This report does not claim a full campaign playthrough.

Older patches and commits remain preserved. Upgrade to the final stable story
patch when available. Bits already erased by an older daily reset cannot be
recovered from that save alone; the sister's Ecruteak/Blackthorn catch-up dialogue
can restore her explained Eevee acquisition, and existing backups remain useful.
