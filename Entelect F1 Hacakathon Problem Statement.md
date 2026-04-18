
max

## 1

## Entelect Grand Prix

## Introduction

Welcome to the start of the brand new Entelect Racing Season! Your task is to create the optimal
race strategy given information about the racetrack layout, your car and the various tyre
compounds available. Your strategy must be resource-efficient and well optimized for speed
around the track to maximize points.

## Goal

As the race strategist, you must develop a program that generates the actions that your car will
take during the race, namely:

- What tyres to use
- Target speed on straights
- When to brake along straights
- When to take a pit stop to change tyres and/or refuel
You will need to consider weather conditions when selecting tyres to optimize how fast you can
safely go around the track. If you take corners too quickly based on your current tyres, their health
and weather conditions, you will suffer a time penalty and greater tyre wear.
You will ultimately be rewarded for completing the race in the fastest time possible while managing
your tyres and fuel effectively; you will receive further score multipliers based on how close you are
to the limit of the resources available to you. Going over the limit will result in a lower score.

## ID6

## Corner

## Braking Point

## ID8

## Corner

## Braking Point

## ID4

## Corner

## ID5

## Corner

## ID3

## Straight

Target Speed: 50 m/s

## ID2

## Corner

## ID1

## Straight

Target Speed: 70 m/s

## ID7

## Straight

Target Speed: 60 m/s

## Braking Point

Visual aid for example level track

## 2

## Assumptions

The following assumptions apply to the race:

## 1. Constant Acceleration

The car accelerates at a constant rate. This rate is defined in the JSON level file.

## 2. Constant Deceleration

The car decelerates at a constant rate. This rate is defined in the JSON level file.

## 3. Limp Mode Trigger

If the car runs out of fuel or your tyre blows during a track segment, the car enters limp
mode. The affected segment and all following segments remain in limp mode until a pit
stop is made to fix the issue.

## 4. Limp Mode Speed

While in limp mode, the car moves at a slow constant speed. There is no acceleration or
deceleration during this time. Limp mode speed is defined in the JSON level file.

## 5. Corner Speed

When entering a corner, the entry speed remains constant for the entire corner. No
acceleration or deceleration occurs while taking the corner.

## 6. Realism

The racetracks are fictional, and are not necessarily realistic in terms of length, corners,
laps or track layout from start to finish. Tyre compound properties are also fictional and are
not necessarily realistic.

## 7. Race Start Speed

The race begins with the car at a speed of 0 m/s.

## 8. Pit Stop Exit Speed

After completing a pit stop, the car exits the pit lane at the pit lane speed. The pit lane
speed is defined in the JSON level file.

## 9. Crawl Mode Trigger

If you take a corner too quickly, the car veers off the track and crashes. The car is then set
to travel at a slow constant speed (i.e. No acceleration) for any subsequent corners until a
straight is encountered to start accelerating again.

## 10. Minimum Speed = Crawl Speed

During the race, the slowest you can travel is at crawl speed. Crawl speed is defined in the
JSON level file.

- Speed follow-through
If you specify a target speed that is slower than your entry speed for a straight, you will just
continue at that entry speed for the rest of that straight.
- SI Units
All values are represented using SI (meters and seconds) units. The JSON properties also
specify the unit of measurement used for the value.

## 3

## Constraints

## Car

Cars have the following properties:

- Acceleration/Deceleration:
o Acceleration is constant on straights. The car will accelerate at a constant rate until
the target speed that you specify is met, after which the car will travel at constant
speed until the braking point.
o Deceleration (braking) is constant on straights. The car will start slowing down at a
constant rate for the remainder of the straight after the braking point.
o Both values are defined in the JSON file.
o Both values are affected by weather; there will be a multiplier that positively or
negatively affects the acceleration and deceleration.

## • Speed Constraints

o The car cannot exceed the Maximum Speed defined in the JSON file.
o Car speed will remain constant for the entire corner.
o Maximum allowed corner speed is determined by the formula below:

max푐표푟푛푒푟푠푝푒푒푑=

## √

## 푡푦푟푒 푓푟푖푐푡푖표푛∗푔푟푎푣푖푡푦∗푟푎푑푖푢푠 +

## 푐푟푎푤푙_푐표푛푠푡푎푛푡_m/s

## • Limp Mode

o Triggered if fuel reaches 0 during a segment OR tyre life span drops to 0 i.e. a
blowout occurs.
o Speed becomes constant, defined by Limp Mode Maximum Speed in the JSON file.
o There is no acceleration or deceleration.
o Applies to all subsequent segments until a pit stop is taken.

## • Crawl Mode

o Triggered if your car takes a corner too quickly i.e. crashes.
o You will travel at the specified crawl mode constant speed. This value is defined in
the JSON file.
o Because you can only accelerate on a straight, this means that you will travel at
crawl mode for any subsequent corners leading up to a straight after a crash.
Time it takes to accelerate from initial speed to final speed:

## 푡푖푚푒=

## 푓푖푛푎푙 푠푝푒푒푑 −푖푛푖푡푖푎푙 푠푝푒푒푑

## 푎푐푐푒푙_푚 /푠푒2

## 4

## Tyres

There are 5 tyre types available:

## • Soft

## • Medium

## • Hard

## • Intermediate

## • Wet

Each tyre compound behaves differently on the track, providing varying levels of friction that affect
how fast a car can take corners. Weather conditions also influence the available friction. If there is
no weather condition specified, it is by default dry.
As tyres wear down, their available friction and life span gradually decreases. When the life span
reaches zero, the tyre blows out, and the car enters limp mode. The car will remain in limp mode
until a pit stop is taken, and the tyres are replaced.
If you choose to change tyres during a pit stop, the tyre’s unique identifier must be referenced in
the pit stop section of the JSON submission. You may switch to a set that is not fully worn by
referencing its unique identifier.

## Soft  Medium  Hard  Intermediate Wet

## Base

## Friction Co-

efficient

## 1.8  1.7  1.6 1.2 1.1

## Dry

## Multiplier

## 1.18 1.08 0.98 0.90 0.72

## Cold

## Multiplier

## 1.00  0.97 0.92 0.96 0.88

## Light Rain

## Multiplier

## 0.92 0.88 0.82 1.08 1.02

## Heavy Rain

## Multiplier

## 0.80 0.74 0.68 1.02 1.20

Dry Rate of

## Degradation

## 0.11 0.10 0.07 0.14 0.16

Cold Rate of

## Degradation

## 0.09 0.08 0.06  0.11 0.12

## Light Rain

Rate of

## Degradation

## 0.12 0.09 0.07 0.08 0.09

## Heavy Rain

Rate of

## Degradation

## 0.13 0.10 0.08 0.09 0.05

## Tyre Properties

As seen in the table above, each tyre has its own appropriate use cases based on the strategy you
have created and the weather forecast. For example:

- Wet tyres
Great in rainy weather, outperformed by other tyres in dry weather.

## 5

- Hard tyres
Great if planning on taking a late pit stop as they have the longest life span among the dry
tyres.
- Soft tyres
Great if planning on taking an early pit stop as they have the shortest life span among the
dry tyres.

## Degradation Type Description

## K_STRAIGHT 0.0000166

## K_BRAKING 0.0398

## K_CORNER 0.000265

## Straights

Your tyre will degrade by the following formula:

푇표푡푎푙 푆푡푟푎푖푔ℎ푡 퐷푒푔푟푎푑푎푡푖표푛 = 푡푦푟푒 푑푒푔푟푎푑푎푡푖표푛 푟푎푡푒 ×track segment length

## × 퐾_푆푇푅퐴퐼퐺퐻푇

## Braking

While braking during a straight, the tyres will degrade by the following formula:

## 퐷푒푔푟푎푑푎푡푖표푛 푤ℎ푖푙푒 퐵푟푎푘푖푛푔=

## (

## (

## 푖푛푖푡푖푎푙푠푝푒푒푑

## 100

## )

## 2

## −

## (

## 푓푖푛푎푙 푠푝푒푒푑

## 100

## )

## 2

## ) × 퐾

## 퐵푅퐴퐾퐼푁퐺

## ×푡푦푟푒 푑푒푔푟푎푑푎푡푖표푛 푟푎푡푒

## Corners

Your tyres will degrade during a corner by the following formula:

## 푇표푡푎푙 퐶표푟푛푒푟 퐷푒푔푟푎푑푎푡푖표푛=퐾

## 퐶푂푅푁퐸푅

## ×

## 푠푝푒푒푑

## 2

## 푟푎푑푖푢푠

## ×푡푦푟푒 푑푒푔푟푎푑푎푡푖표푛 푟푎푡푒

## Tyre Friction

To calculate the amount of friction on your tyres at any given point, use the formula below:

## 푡푦푟푒 푓푟푖푐푡푖표푛=

## (

## 푏푎푠푒푓푟푖푐푡푖표푛푐표푒푓푓푖푐푖푒푛푡−푡표푡푎푙푑푒푔푟푎푑푎푡푖표푛

## )

## ×

## 푤푒푎푡ℎ푒푟푚푢푙푡푖푝푙푖푒푟

Example: Soft tyre in dry weather that has accumulated a total degradation of 0.5:

## 푡푦푟푒 푓푟푖푐푡푖표푛 =

## (

## 1.8−0.5

## )

## ×

## (

## 1

## )

## =

## (

## 1.3

## )

## ×

## (

## 1

## )

## = 1.3

## 6

## Fuel

Fuel consumption depends on the speed of the car during the race. Driving at higher speeds will
result in higher fuel usage. You must therefore balance speed and fuel efficiency to ensure that the
car can complete the race without running out of fuel.
In Level 1, there are no fuel limitations, allowing you to become familiar with the race simulation. In
later levels, fuel management becomes an important factor, you must make conscious choices
about your fuel usage.

## Fuel Usage

## • 푲

## 풃풂풔풆

: Base fuel consumption rate: 0.0005 l/m

## • 푲

## 풅풓풂품

: Fuel consumption based on distance: 0.0000000015 l/m

## Fuel Usage Formula

## 퐹

## 푢푠푒푑

## = (푲

## 풃풂풔풆

## +푲

## 풅풓풂품

## (

## 푖푛푖푡푖푎푙 푠푝푒푒푑+푓푖푛푎푙 푠푝푒푒푑

## 2

## )

## 2

## ) ×푑푖푠푡푎푛푐푒

## Example

- Initial speed 푣

## 푖

=50 m/s

- Final speed 푣

## 푓

=70 m/s

- Distance 푑=800 m

## 퐹

## 푢푠푒푑

## = (0.0005 +0.0000000015

## (

## 50+70

## 2

## )

## 2

## ) ×800

## =0.40432 푙푖푡푟푒푠

## Refueling

When refueling during a pit stop, the time taken is dependent on the amount of fuel you are filling
up. The time it takes to refuel your car is shown below:

Pit Stop Refuel formula:

## 푟푒푓푢푒푙 푡푖푚푒 (푠) =

## 푎푚표푢푛푡 푡표 푟푒푓푢푒푙 (퐿)

## 푟푒푓푢푒푙 푟푎푡푒 (퐿/푠)

Example: Refuel 30l with a refuel rate of 10 l/s:

## 푟푒푓푢푒푙 푡푖푚푒

## (

## 푠

## )

## =

## 30

## 10

## =3 푠푒푐표푛푑푠

## 7

## Track

A track is an ordered list of segments (straights and corners).
Each segment has the following properties:

## • Length (m)

## • Type

- Radius (only for corners)
Please refer to the Tyres section for the formula and examples of calculating tyre friction.
The track also includes a pit lane entry which is accessible only at the end of the lap.

## Straights

- You need to define your target speed for that straight.
- You must specify in your JSON submission the point in the straight (in m) at which braking
begins.

## Corners

- Corners have a maximum speed at which the car can safely take it based on the current
tyre friction and the radius of the corner.
- Exceeding this maximum speed will cause the car to veer off track and crash, resulting in a
time penalty and major tyre degradation.
- The time penalty for crashing is defined in the JSON file as corner_crash_penalty_s.
- Maximum allowed corner speed is determined by the below formula:

## 푀푎푥푐표푟푛푒푟푠푝푒푒푑=

## √

## 푡푦푟푒 푓푟푖푐푡푖표푛∗푔푟푎푣푖푡푦∗푟푎푑푖푢푠 + 푐푟푎푤푙_푐표푛푠푡푎푛푡_m/s

Example: Tyre friction of 0.9, gravity constant of 9.8 and a corner radius of 50:

## 푀푎푥푐표푟푛푒푟푠푝푒푒푑=

## √

## 0.9∗9.8∗50 + 10

=  31 m/s

## 8

## Pit Stops

The pit lane is only accessible at the end of the lap. The pit lane is not a segment that forms part of
the track but can be optionally entered at the end of the track.
The following options are available for pit stops:

- Change tyres

## • Refuel

- Both changing tyres and refueling
When making a pit stop, you must specify which tyres you are switching to (by providing the tyre ID)
and the amount of fuel you want to fill up. If either of these values are not provided or are zero, it is
assumed that you are not making that change.
The time taken for the pit stop depends on:
- Pit tyre swap time (defined in JSON)
- Amount wanting to be refueled (this is a rate in l/s defined in JSON)
- Base pit stop time (defined in JSON)

## Formula

## 푝푖푡 푠푡표푝 푡푖푚푒

## (

## 푠

## )

## =푟푒푓푢푒푙 푡푖푚푒+푝푖푡 푡푦푟푒 푠푤푎푝 푡푖푚푒+푏푎푠푒 푝푖푡 푠푡표푝 푡푖푚푒

Example: Pit stop consisting of refueling 30l with a rate of 10l/s, tyre change with a time of 5s, and
base pit stop time of 20s:

## 푝푖푡 푠푡표푝 푡푖푚푒

## (

## 푠

## )

## =

## (

## 30

## 10

## )

## +5+20

## =28 푠푒푐표푛푑푠

## 9

## Weather

During the race, the weather conditions will change at specific times. This change will be provided
in the level JSON file. If there is no weather condition specified, it is by default dry.
The weather change has the following properties:

- Time of weather change
- Duration of weather conditions (If the race time is long enough that all weather conditions
have been cycled through, it starts again from the first weather condition)
The weather conditions affect different aspects of the race, namely:

## • Acceleration

## • Deceleration

- Tyre wear
There are 4 types of weather conditions:

## • Dry

## • Cold

## • Light Rain

## • Heavy Rain

As seen in the tyre section, each tyre compound has different wear rates and friction multipliers
based on the weather.

## Penalties

You will incur penalties for the following actions:

- Taking a corner too fast results in increased tyre wear, a time penalty and the car entering
crawl mode.
- The time penalty is configured in the JSON as the corner_crash_penalty_s property and is
added to your current lap time at the time of the crash.
- The tyre penalty is a flat 0.1 degradation to the current tyre set.
- Crawl mode causes the car to travel at a constant speed until another straight is
encountered to start accelerating again.
- Running out of fuel OR experiencing a tyre blowout results in the car entering limp mode.
- Limp mode causes the car to travel at limp mode constant speed until a pit stop is taken to
refuel and/or change tyres.

## 10

## Levels

Each level file defines the characteristics of the race, including the car, track, tyres, and other
parameters.
All race factors must be considered when developing your race strategy for submission. Each level
adds new factors while building on the previous ones (i.e. Level 2 contains the rules from level 1, in
addition to its own).

## Level 1

Basic rules to help get you familiar with the problem and achieve the best possible race time. Your
focus will be on the following:

- Navigating the track.
- Choosing when to brake on straights.
- Defining the target speed on straights.
- Entering corners at an appropriate speed to safely take them.
- Choosing the appropriate tyre compound to start the race with – tyres do not degrade in
level 1.

## Level 2

Fuel management and pit stops are introduced. In addition to level 1, focus on:

- Managing fuel usage by adjusting your target speeds per segment.
- Tracking fuel usage.
- Taking pit stops to refuel.
- Avoiding running out of fuel during the race to prevent entering limp mode.
- Optimizing race time and fuel usage to maximize the fuel efficiency multiplier at the end for
scoring.
- The fuel allowance for the race is a ‘soft cap’, it may exceed but the more you go over, the
more negatively your score will be affected.

## Level 3

Weather is introduced, which greatly affects tyre and pit stop strategies. In addition to previous
levels, focus on:

- Keeping track of the race time and when the weather will change.
- Choosing the correct tyre for the weather conditions.
- Pitting for tyre changes when the weather conditions change.
- Adjusting target speeds and braking points as the friction of the tyres are affected by
weather changes.

## 11

## Level 4

A large focus on tyre degradation and how tyre performance changes as the more it gets used. In
addition to the previous levels, focus on:

- Keeping track of tyre degradation and overall tyre health.
- Adjusting target speeds and braking points as tyres degrade.
- Taking pit stops to avoid tyre blowouts and entering limp mode.
- Managing a limited set of available tyres and tyre compounds.
- Optimizing race time and tyre usage to use as much tyre health as possible to maximize the
tyre efficiency multiplier at the end for scoring.

## 12

## Scoring

The following formulas will be used for scoring on each of the different levels.

## Level 1

A time penalty is applied whenever a player has exceeded the maximum speed at which a corner
can be taken.  This time penalty is defined in the level 1 JSON file as the corner_crash_penalty_s
property under race. Each level also has it’s own reference time as the time_reference_s property
under race.

## 풃풂풔풆풔풄풐풓풆=500 000

## (

## 푡푖푚푒_푟푒푓푒푟푒푛푐푒_푠

## 푡푖푚푒

## )

## 3

## Level 2 & Level 3

## 풇풖풆풍 풃풐풏풖풔= −500 000

## (

## 1−

## 푓푢푒푙 푢푠푒푑

## 푓푢푒푙_푠표푓푡_푐푎푝_푙푖푚푖푡_푙

## )

## 2

## +500 000

## 풇풊풏풂풍 풔풄풐풓풆 = 푏푎푠푒 푠푐표푟푒 +  푓푢푒푙 푏표푛푢푠

## Level 4

풕풚풓풆 풃풐풏풖풔= 100 000 ×∑푡푦푟푒 푑푒푔푟푎푑푎푡푖표푛  − 50 000 ×number of blowouts

## 풇풊풏풂풍 풔풄풐풓풆 = 푏푎푠푒 푠푐표푟푒 + 푡푦푟푒 푏표푛푢푠 + 푓푢푒푙 푏표푛푢푠

## 13

## Submissions

Participants must submit their solution on the Entelect Hackathon website. The submission must
include two items:

- A ZIP of the source code.
- A .txt file containing the output.
The solution must be deterministic, meaning that given the same input, the program must always
produce the same output. During validation, the submitted source code will be executed to
reproduce the results provided in the submission. If the source code does not produce the same
output as the submitted file, the submission will be considered invalid.
The .txt file must contain a valid JSON object describing the race configuration which should
include the following key information:
- Initial tyre id
- Actions taken during each segment in each lap

## {

## "initial_tyre_id": 1

## "laps": [

## {

## "lap": 1

## "segments": [

## {

## "id": 1

## "type": "straight"

## "target_m/s": 70

## "brake_start_m_before_next": 800

## }

## {

## "id": 2

## "type": "corner"

## }

## {

## "id": 3

## "type": "straight"

## "target_m/s": 50

brake_start_m_before_next": 500

## }

## {

## "id": 4

## "type": "corner"

## }

## {

## "id": 5

## "type": "corner"

## }

## {

## "id": 6

## "type": "corner"

## 14

## }

## {

## "id": 7

## "type": "straight"

## "target_m/s": 60

## "brake_start_m_before_next": 500

## }

## {

## "id": 8

## "type": "corner"

## }

## ]

## "pit": {

"enter": false

## }

## }

## {

## "lap": 2

## "segments": [

## {

## "id": 1

## "type": "straight"

## "target_m/s": 70

## "brake_start_m_before_next": 800

## }

## {

## "id": 2

## "type": "corner"

## }

## {

## "id": 3

## "type": "straight"

## "target_m/s": 50

## "brake_start_m_before_next": 500

## }

## {

## "id": 4

## "type": "corner"

## }

## {

## "id": 5

## "type": "corner"

## }

## {

## "id": 6

## "type": "corner"

## }

## 15

## {

## "id": 7

## "type": "straight"

## "target_m/s": 60

## "brake_start_m_before_next": 500

## }

## {

## "id": 8

## "type": "corner"

## }

## ]

## "pit": {

"enter": true,

## "tyre_change_set_id": 3

## "fuel_refuel_amount_l": 20

## }

## }

## ]

## }

## Example: Submission

## 16

## Appendix

## Objects

## Car

## Property Name

JSON Property

## Name

Unit of

## Measurement

## Explanation

Maximum Speed max_speed_m/s
Meters per
second
The maximum speed the
car can reach at any point
on the track.
Acceleration accel_m/se2

Meters per
second

## 2

The constant rate at which
the car increases speed on
straight segments.
Deceleration brake_m/se2
Meters per
second

## 2

The constant rate at which
the car reduces speed
when slowing down for
corners on straight
segments.
Limp Mode Speed limp_constant_m/s
Meters per
second
The speed the car travels at
while operating in limp
mode.
Crawl Mode Speed crawl_constant_m/s
Meters per
second
The speed the car travels at
while operating in crawl
mode.
Fuel Tank Capacity fuel_tank_capacity_l Litres
The maximum amount of
fuel the car’s fuel tank can
hold.
Initial Fuel initial_fuel_l Litres
The amount of fuel in the
car at the start of the race.

## 17

## Race

Property Name JSON Property Name
Unit of

## Measurement

## Explanation

Race Name name N/A The name of the race.
Number of Laps laps N/A
The total number of laps for
the race.

## Pit Stop Tyre

## Change Time

pit_tyre_swap_time_s Seconds
The time taken to change
tyres during a pit stop.

## Base Pit Stop

## Time

base_pit_stop_time_s Seconds
The base time taken in the
pit lane.
Pit Stop Tyre and

## Fuel Time

pit_refuel_rate_l/s Litres/second
The rate at which refueling
is done in litres per second.

## Corner Crash

## Penalty

corner_crash_penalty_s Seconds
A time penalty applied
when a car takes a corner
too fast and veers off the
track.
Pit Exit Speed pit_exit_speed_m/s Meters/second
The speed at which you
start at when exiting the pit
lane.

## Fuel Soft Cap

## Limit

fuel_soft_cap_limit Litres
The soft cap limit for the
fuel, if exceeded you will
lose your fuel bonus.

## Starting Weather

## Conditions

starting_weather_condition N/A
The weather condition at
the start of the race.

## 18

## Track

Property Name JSON Property Name
Unit of

## Measurement

## Explanation

Track Name name N/A The name of the track.
Track Segments segments N/A
A list of all segments that
make up the track.
Segment ID id N/A
The id of the track segment as
they appear in order during
the race.
Segment Type type N/A The type of track segment.
Segment Length length_m Meters
The length of the track
segment in m.
Corner Radius radius_m Meters
The radius of the corner. This
value is used to calculate the
maximum speed when taking
the corner.

## 19

## Tyres

Property Name JSON Property Name
Unit of

## Measurement

## Explanation

## Available Tyre

## Sets

available_sets N/A List of available tyre sets.
Tyre IDs ids N/A
List of tyre IDs available
per compound set.
Tyre Compound compound N/A
The type of tyre
compound for the set.
Tyre Life Span life_span N/A
The amount of friction
that the tyre set starts
with.

## Dry Friction

## Multiplier

dry_friction_multiplier Multiplier
Multiplier used for friction
when in dry weather
conditions.

## Cold Friction

## Multiplier

cold_friction_multiplier Multiplier
Multiplier used for friction
when in cold weather
conditions.

## Light Rain

## Friction

## Multiplier

light_rain_friction_multiplier Multiplier
Multiplier used for friction
when in light rain weather
conditions.

## Heavy Rain

## Friction

## Multiplier

heavy_rain_friction_multiplier Multiplier
Multiplier used for friction
when in heavy rain
weather conditions.
Dry Degradation dry_degradation N/A
Rate at which tyres
degrade in dry weather
conditions.

## Cold

## Degradation

cold_degradation N/A
Rate at which tyres
degrade in cold weather
conditions.

## Light Rain

## Degradation

light_rain_degradation N/A
Rate at which tyres
degrade in light rain
weather conditions.

## Heavy Rain

## Degradation

heavy_rain_degradation N/A
Rate at which tyres
degrade in heavy rain
weather conditions.

## 20

## Weather

Property Name JSON Property Name
Unit of

## Measurement

## Explanation

Weather condition condition N/A Type of weather condition.
Weather ID id N/A
The unique identifier for the
weather condition.
Duration of

## Weather

## Conditions

duration_s seconds
The duration that the weather
conditions will last for.

## Acceleration

## Multiplier

acceleration_multiplier N/A
The value by which the
acceleration constant is
affected due to weather.

## Deceleration

## Multiplier

deceleration_multiplier N/A
The value by which the
deceleration constant is
affected due to weather.

## 21

JSON file example
A race is represented using a JSON file. An example of this file for level 4 is shown below:

## {

## "car": {

## "max_speed_m/s": 90

## "accel_m/se2": 10

## "brake_m/se2": 20

## "limp_constant_m/s": 20

## "crawl_constant_m/s": 10

## "fuel_tank_capacity_l": 150.0

## "initial_fuel_l": 150.0

## "fuel_consumption_l/m": 0.0005

## }

## "race": {

"name": "Entelect GP Level 0",

## "laps": 2

## "base_pit_stop_time_s": 20.0

## "pit_tyre_swap_time_s": 10.0

## "pit_refuel_rate_l/s": 5.0

## "corner_crash_penalty_s": 10.0

## "pit_exit_speed_m/s": 20.0

## "fuel_soft_cap_limit_l": 1400.0

## "starting_weather_condition_id": 1

## "time_reference": 7300.0

## }

## "track": {

"name": "Neo Kyalami Example",

## "segments": [

## {"id": 1, "type": "straight", "length_m": 850}

## {"id": 2, "type": "corner", "radius_m": 60, "length_m": 120}

## {"id": 3, "type": "straight", "length_m": 850}

## {"id": 4, "type": "corner", "radius_m": 60, "length_m": 120}

## {"id": 5, "type": "corner", "radius_m": 45, "length_m": 90}

## {"id": 6, "type": "corner", "radius_m": 80, "length_m": 140}

## {"id": 7, "type": "straight", "length_m": 650}

## {"id": 8, "type": "corner", "radius_m": 80, "length_m": 140}

## ]

## }

## "tyres": {

## "properties": {

"Soft": {

## "life_span": 1

## "dry_friction_multiplier": 1.18

## "cold_friction_multiplier": 1.00

## "light_rain_friction_multiplier": 0.92

## "heavy_rain_friction_multiplier": 0.80

## 22

## "dry_degradation": 0.14

## "cold_degradation": 0.11

## "light_rain_degradation": 0.12

## "heavy_rain_degradation": 0.13

## }

"Medium": {

## "life_span": 1

## "dry_friction_multiplier": 1.08

## "cold_friction_multiplier": 0.97

## "light_rain_friction_multiplier": 0.88

## "heavy_rain_friction_multiplier": 0.74

## "dry_degradation": 0.10

## "cold_degradation": 0.08

## "light_rain_degradation": 0.09

## "heavy_rain_degradation": 0.10

## }

"Hard": {

## "life_span": 1

## "dry_friction_multiplier": 0.98

## "cold_friction_multiplier": 0.92

## "light_rain_friction_multiplier": 0.82

## "heavy_rain_friction_multiplier": 0.68

## "dry_degradation": 0.07

## "cold_degradation": 0.06

## "light_rain_degradation": 0.07

## "heavy_rain_degradation": 0.08

## }

"Intermediate": {

## "life_span": 1

## "dry_friction_multiplier": 0.90

## "cold_friction_multiplier": 0.96

## "light_rain_friction_multiplier": 1.08

## "heavy_rain_friction_multiplier": 1.02

## "dry_degradation": 0.11

## "cold_degradation": 0.09

## "light_rain_degradation": 0.08

## "heavy_rain_degradation": 0.09

## }

"Wet": {

## "life_span": 1

## "dry_friction_multiplier": 0.72

## "cold_friction_multiplier": 0.88

## "light_rain_friction_multiplier": 1.02

## "heavy_rain_friction_multiplier": 1.20

## "dry_degradation": 0.16

## "cold_degradation": 0.12

## "light_rain_degradation": 0.09

## 23

## "heavy_rain_degradation": 0.05

## }

## }

## }

## "available_sets": [

## {

## "ids": [1, 2, 3]

"compound": "Soft"

## }

## {

## "ids": [4, 5, 6]

"compound": "Medium"

## }

## {

## "ids": [7, 8, 9]

"compound": "Hard"

## }

## {

## "ids": [10, 11, 12]

"compound": "Intermediate"

## }

## {

## "ids": [13, 14, 15]

"compound": "Wet"

## }

## ]

## "weather": {

## "conditions": [

## {

## "id": 1

## "condition": "cold"

## "duration_s": 1000.0

## "acceleration_multiplier": 0.95

## "deceleration_multiplier": 0.95

## }

## {

## "id": 2

## "condition": "light_rain"

## "duration_s": 3000.0

## "acceleration_multiplier": 0.80

## "deceleration_multiplier": 0.80

## }

## ]

## }

## }

Race Representation JSON

## 24

## Terms

## Term Explanation

Straight A section of the track that is straight with no curves
Pit Lane The section of the racetrack where cars enter to switch tyres or refuel

## Corner

Section of the track that curves where cars need to travel below a certain
speed to safely take the turn
Braking Point This is the part of the straight at which you start braking to slow down

## Calculations & Algorithms

N.B. All values are in SI units
Speed required to cover a certain distance at a certain time:

## 푠푝푒푒푑=

## 푙푒푛푔푡ℎ_푚

## 푡푖푚푒

Distance if final speed is known instead of time:

## 푙푒푛푔푡ℎ =

## 푓푖푛푎푙 푠푝푒푒푑

## 2

## −푖푛푖푡푖푎푙 푠푝푒푒푑

## 2

## 2 ×푎푐푐푒푙_푚푝푠

## 2

Distance if time is known instead of final speed:

## 푙푒푛푔푡ℎ=푖푛푖푡푖푎푙 푠푝푒푒푑

## (

## 푡푖푚푒

## )

## +0.5

## (

## 푎푐푐푒푙_푚푝푠

## 2

## )(

## 푡푖푚푒

## )

## 2
