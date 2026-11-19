## The machines

**The short version:** A sampler is a digital recorder you can play like an instrument: it measures a sound thousands of times a second, stores the numbers and reads them back at whatever pitch you ask for.[^mac-izotope-basics] The first commercial one, the Fairlight CMI of 1979, was an 8-bit computer with a light pen and a five-figure price in pounds.[^mac-120years-fairlight][^mac-museumsvic-fairlight] Eight years later a drum box with 10 seconds of 12-bit memory was setting the sound of hip-hop, and its flaws were kept on purpose when the maker reissued it in 2021.[^mac-rossum-sp1200]

### How does a sampler work?

A record or a microphone hands the sampler a smoothly moving signal. The sampler measures it at regular ticks and writes each measurement down as a number. Read the numbers back at the same speed and the sound returns; read them faster or slower and it comes back higher or lower, the way a turntable does when you change its speed. Two settings decide how good the copy is.

**Sample rate** is how many measurements are taken each second, and it sets the highest pitch the machine can capture.[^mac-izotope-basics] The Nyquist rule says the top frequency is half the sample rate, so 44.1 kHz, the rate the CD made standard, reaches 22.05 kHz.[^mac-izotope-basics] Sound above that limit does not vanish. It folds back as a false lower tone, an effect called **aliasing**: a 30,000 Hz harmonic sampled at 44.1 kHz reappears at 14,100 Hz.[^mac-mixdown-terms] A low-pass filter in front of the converter is there to stop it.[^mac-izotope-basics]

**Bit depth** is how many loudness steps each measurement can land on: 2 to the power of the bit depth, with about 6 dB of dynamic range for every bit.[^mac-izotope-basics] Each measurement gets rounded to the nearest step, and the rounding error is heard as **quantization noise**.[^mac-izotope-basics]

| Bit depth | Loudness steps | Dynamic range | Where you meet it |
|---|---|---|---|
| 8-bit | 256 | about 48 dB | Fairlight CMI Series I, Casio SK-1 |
| 12-bit | 4,096 | about 72 dB | E-mu SP-1200, Akai S900, Akai MPC60 |
| 16-bit | 65,536 | about 96 dB | Akai S1000, EP-133 K.O. II |
| 24-bit | 16,777,216 | about 144 dB | Akai MPC4000 |

The 16-bit and 24-bit figures are the published ones; the 8-bit and 12-bit rows are the same formula run on smaller numbers.[^mac-izotope-basics][^mac-mixdown-terms]

The third limit was memory. Every second of sound costs the sample rate multiplied by the bit depth, and in the 1980s that bill was steep. An Akai S900 could spread its 750 KB over 63 seconds by dropping to 7.5 kHz, or spend it all on a little under 12 seconds at top quality.[^mac-vse-s900][^mac-perfectcircuit-sseries] Every early sampler owner made some version of that trade, usually several times a session.

### What was the first sampler?

The tape-era ancestors - musique concrète, the Chamberlin and the Mellotron - are at [/history/](/history/).

The Fairlight CMI came out of Sydney, where Peter Vogel and Kim Ryrie built it on the bones of Tony Furse's Qasar M8, a 1975 design.[^mac-120years-fairlight] It was demonstrated in 1979, ran on two 8-bit 6800 processors, and let you poke at its screen with a light pen. Museums Victoria, which holds one, calls it the first commercially available digital sampling instrument.[^mac-museumsvic-fairlight] The Series I sampled at 8-bit and 24 kHz across eight voices. The Series II of 1982 raised the rate to 32 kHz and added Page R, a pattern sequencer. The Series III of 1985 went to 16-bit, 50 kHz stereo and 16 voices.[^mac-120years-fairlight]

What one cost depends on who is telling it. One history gives £18,000 for the first model, £27,000 for the Series II and £60,000 for the Series III.[^mac-120years-fairlight] Wikipedia has £12,000 as the UK price, US$27,500 for each of the units sold in the US in 1980, and £30,000 for the Series II.[^mac-wiki-fairlight] Reverb says £13,000.[^mac-reverb-ensoniq] The first customers are just as slippery: the museum record has Peter Gabriel and Stevie Wonder buying the first units in 1979, while Wikipedia has Wonder and Herbie Hancock buying in 1980 and John Paul Jones as the first UK customer.[^mac-museumsvic-fairlight][^mac-wiki-fairlight]

E-mu's Emulator followed in 1981 and sold about 500 units before it was dropped in early 1984.[^mac-musicradar-emulator][^mac-wiki-emulator] Its price is given as $8,000 in one account and "£8050" in another, which reads like the same number wearing a different currency sign.[^mac-reverb-ensoniq][^mac-musicradar-emulator] The first unit had been promised to Daryl Dragon until Stevie Wonder placed an order.[^mac-musicradar-emulator] The Emulator II arrived in 1984, at a reported $7,995.[^mac-sos-emulator2][^mac-wiki-emulator]

### When did samplers get cheap?

In 1984 the Ensoniq Mirage went on sale at $1,695, when an Emulator ran about $8,000.[^mac-reverb-ensoniq] Ensoniq had been founded by three former Commodore engineers, Bruce Crockett, Al Charpentier and Bob Yannes.[^mac-reverb-ensoniq] Cheap came with conditions: Hank Shocklee, who made early Public Enemy records on a Mirage, remembered having about three seconds of sample time.[^mac-reverb-ensoniq]

The floor dropped further with the Casio SK-1, a toy-sized keyboard that sold for under $100. It had a built-in microphone, four voices, 8-bit sound and 1.4 seconds of sampling, enough for one word or one dog bark. It later became a standard choice for circuit bending.[^mac-musicradar-sk1]

### Why does the SP-1200 sound like that?

Because it is a 12-bit machine sampling at 26.04 kHz, and because of what happens when it changes pitch. Dave Rossum designed it.[^mac-rossum-sp1200] Half of 26.04 kHz is 13.02 kHz, so the top of the record is gone before the drums ever reach a pad. Re-tuning a sound on the SP-1200 adds what Rossum's company calls "aliasing and imaging artifacts", and the company kept them on purpose in its reissue.[^mac-rossum-sp1200] The Village Voice called the result "gritty 12-bit sound quality" and credited the machine for crunchy drums, choppy samples and murky filtered basslines.[^mac-voice-sp1200] The producer Ski put it in two words: "so dirty."[^mac-voice-sp1200]

The E-mu SP-12 came first, in 1985, and the SP-1200 replaced it in 1987.[^mac-rossum-sp1200] The US launch prices in circulation, $2,745 and $2,995, come from Wikipedia alone; Sound On Sound's October 1987 review listed the SP-1200 in Britain at £2,199 including VAT.[^mac-wiki-sp1200][^gfa-sos-sp1200-1987] The SP-1200 held 10 seconds of sound in total, and no single sound could run longer than 2.5 seconds, because of what RAM cost in 1987.[^mac-rossum-sp1200] The Village Voice, citing the manufacturer, makes it 10.07 seconds; Hank Shocklee, from memory, said 12.[^mac-voice-sp1200] Its eight outputs are not alike either: channels 1 and 2 pass through SSM2044 filters, 3 to 6 have fixed filters, and 7 and 8 have none.[^mac-rossum-sp1200]

Ten seconds is not much, so producers cheated. Shocklee again: "You take a 33 1/3 record and play it on 45, and you cheat the system."[^mac-voice-sp1200] The record goes in fast and high, and the pad is tuned back down afterward, one of the moves at [/making-a-flip/](/making-a-flip/). The arithmetic is friendly. 45 divided by 33 1/3 is 1.35, so 10 seconds of memory swallows about 13.5 seconds of record. Tuning the sound back down also lowers its effective sample rate, which is one more layer of dirt on a machine already known for it.

Rossum Electro-Music sold a reissue from 2021 to 2025 at $3,999 with 20 seconds of memory, and closed the line with a 40th Anniversary Edition of 100 units at $4,999.[^mac-rossum-sp1200]

### What did the Akai S900 and S950 add?

Time. The Akai S900 of 1986 was a 12-bit sampler with eight voices, room for 32 samples and a sample rate you could set anywhere from 7.5 to 40 kHz.[^mac-vse-s900] The S950 that followed in 1988 pushed the top rate to 48 kHz and could be expanded from 750 KB to 2,250 KB; a British review in March 1989 priced it at £1,399 including VAT and measured 9.89 seconds at full quality on the base unit.[^mac-vse-s900][^mac-muzines-s950]

The S950 also brought **time-stretch**, which changes how long a sound lasts without changing its pitch. It could stretch from 1% to 999% and might take up to 91 seconds to think about it.[^mac-muzines-s950] One retailer history calls it the first sampler of its kind with the feature.[^mac-perfectcircuit-sseries] The S1000 then moved the series to 16-bit stereo at 44.1 kHz, the sample rate of the CD, with 2 MB of memory expandable to 8 MB.[^mac-perfectcircuit-sseries]

### Who designed the MPC?

Two people. Roger Linn did the functional design and the interface of the Akai MPC60, and David Cockerell built the sound engine.[^mac-musicradar-mpc] It came out in 1988 at a reported $5,000: 12-bit, 40 kHz, 16 pads, a 99-track sequencer, and 13.1 seconds of sampling that an upgrade doubled to 26.2.[^mac-musicradar-mpc][^mac-vse-mpc60] Its voice count is given as both 16 and 18.[^mac-vse-mpc60]

The line that followed is long. The MPC60II came in 1991 and the MPC3000 in 1994, with 32 voices, a filter and effects, and Linn still involved.[^mac-musicradar-mpc] The MPC2000 of 1997 was 16-bit and designed without him; the MPC2000XL followed in 1999 and the 24-bit MPC4000 in 2002.[^mac-musicradar-mpc][^mac-reverb-mpc-timeline][^mac-perfectcircuit-mpc]

One MPC is now a museum object. J Dilla's MPC3000 Limited Edition, one of about 2,000 made in 2000, was given to the Smithsonian's National Museum of African American History and Culture by his mother, Maureen Yancey, in a donation announced in July 2014.[^mac-smithsonian-dilla]

### What is MPC swing?

A delay on every other 16th note, and nothing more mysterious than that. Linn's own description: "I merely delay the second 16th note within each 8th note."[^mac-attack-linn] The setting is a percentage. At 50% the two 16th notes are even and there is no swing; at 66% the pair becomes a triplet.[^mac-attack-linn] The useful territory is in between. Linn says 54% loosens a straight beat without making it sound swung, and that 62% at 90 BPM feels looser than a full 66%.[^mac-attack-linn]

He ranks swing first among six reasons for the MPC's feel and is unsentimental about the rest: "Not much magic," he told Attack Magazine in 2013.[^mac-attack-linn] He also says he introduced recording **quantization**, the snapping of played notes to a timing grid, on his LM-1 drum machine in 1979.[^mac-attack-linn] The Alchemist, a working user, says the dial runs from 50 to 75 and that he likes 62 or 63.[^mac-musicradar-mpc]

### What is the ASR-10?

Ensoniq's sampler of 1992, and the answer to a lot of "what did they make that on" questions. It descended from the 13-bit EPS of 1988 and the 16-bit EPS 16+ of 1990.[^mac-reverb-ensoniq] Its users include RZA, Kanye West, Timbaland, The Neptunes, Prince Paul and The Alchemist.[^mac-reverb-ensoniq] RZA's summary: "The whole first 100 Wu-Tang songs was made on an ASR-10."[^mac-reverb-ensoniq]

### Why do beatmakers love the SP-303 and SP-404?

Madlib made three tracks on Madvillainy in a hotel room in Brazil with a Boss SP-303, a portable turntable and a cassette deck.[^mac-reverb-sp404] That is the pitch for the whole SP line: a sampler small enough to pack.

It began with the Boss SP-202 Dr. Sample in 1998, with eight pads and 4 minutes 20 seconds of sampling.[^mac-roland-samplers] The SP-303 of 2001 added a tape echo and Vinyl Sim, an effect that imitates a worn record; Roland's own history credits it on Madvillainy and on J Dilla's Donuts, and names Four Tet and Animal Collective as users.[^mac-roland-samplers] The SP-505 followed in 2002 and the SP-606 in 2004.[^mac-reverb-sp-timeline]

The Roland SP-404 of 2005 had 12 pads, 29 effects and a CompactFlash slot, and became the instrument of a beat scene that includes Flying Lotus, Ras G and Dibia$e.[^mac-roland-samplers][^mac-reverb-sp404] The SP-555 came in 2008 and the SD-card SP-404SX in 2009.[^mac-reverb-sp-timeline] The SP-404A is dated 2014 in one timeline and 2017 in Roland's own article.[^mac-reverb-sp-timeline][^mac-roland-samplers] The SP-404MKII of 2021 has an OLED screen, 16 GB of storage and Skip Back Sampling.[^mac-roland-samplers]

### What sampler should a beginner know about?

There are more answers than there used to be, and none of them costs what a Fairlight did.

The Teenage Engineering EP-133 K.O. II launched in November 2023 at $299 (€349, £299) with 12 pads, 999 sample slots, 64 MB of memory and 16-bit sound at about 46 kHz.[^mac-cdm-ko2][^mac-sos-ko2] In January 2026 a 128 MB version at $329 became the standard model and the 64 MB one was discontinued.[^mac-synthanatomy-ko2]

The Akai MPC One, from 2020, is a standalone MPC with a 7-inch touchscreen and no battery, reviewed at $699 / £639.[^mac-sos-mpcone] It belongs to a generation that began in 2017 with the MPC Live and MPC X, which run the MPC software on the device itself; the MPC Live III of 2025 can pull a finished mix apart into stems on board, a trick covered at [/ai/](/ai/).[^mac-reverb-mpc-timeline][^mac-musicradar-mpc] The SP-404MKII is the current member of the SP line described above.[^mac-roland-samplers]

Native Instruments' Maschine started in 2009 as a pad controller that needed a computer. The Maschine+ runs on its own and was reviewed in January 2021 at $1,399 / £1,099.[^mac-sos-maschineplus]

On a computer, Ableton Live has been stretching audio to the song's tempo since its release on October 30, 2001.[^mac-musicradar-live20] Early versions wanted warp markers placed by hand; Auto-Warp arrived in Live 5.[^mac-musicradar-live20] Co-founder Gerhard Behles wrote the first stretch algorithm himself and is candid about it: "It was worse than any of the algorithms we use today."[^mac-zplane-behles] For Live 5, Ableton licensed zplane's élastique, which became the "Complex" mode.[^mac-zplane-behles] Serato Sample, a plug-in announced as a public beta on April 27, 2017, finds the key, sets cue points and chops, stretches and re-pitches inside whatever software hosts it, using the Pitch 'n Time engine Serato first released in 1998.[^mac-fact-serato][^mac-serato-story]

The cheapest sampler in the list is a phone app. Koala Sampler, written by Marek Bereza of Elf Audio and modeled on the Boss SP-303, arrived on iOS in March 2019 at $2.99: record up to 64 sounds through the phone's microphone, run them through eight effects, sequence them and export a WAV.[^gfa-synthtopia-koala-2019] By October 2022 it was on Android too, at $4.99 / £4.49, with resampling and paid add-ons for time-stretching and slicing.[^gfa-sos-koala-2022]

| Machine | Year | Resolution | Sample time or memory | Launch price, as reported |
|---|---|---|---|---|
| Fairlight CMI Series I | 1979 | 8-bit, 24 kHz | - | £18,000, £12,000 or £13,000 |
| E-mu Emulator | 1981 | - | - | $8,000 |
| Ensoniq Mirage | 1984 | - | about 3 seconds, as Shocklee recalled | $1,695 |
| E-mu SP-1200 | 1987 | 12-bit, 26.04 kHz | 10 seconds; 2.5 per sound | $2,995 (Wikipedia); £2,199 inc VAT (1987 review) |
| Akai S900 | 1986 | 12-bit, 7.5-40 kHz | 750 KB; under 12 seconds at top rate | - |
| Akai S950 | 1988 | 12-bit, up to 48 kHz | 9.89 seconds at 48 kHz | £1,399 inc VAT (1989 review) |
| Akai MPC60 | 1988 | 12-bit, 40 kHz | 13.1 seconds; 26.2 expanded | $5,000 |
| Boss SP-202 | 1998 | - | 4 min 20 s | - |
| Akai MPC One | 2020 | - | - | $699 / £639 |
| EP-133 K.O. II | 2023 | 16-bit, about 46 kHz | 64 MB | $299 / €349 |

[[MODULE:machines]]
