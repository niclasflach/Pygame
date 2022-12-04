## Simulation of organisms(Blobs) in Pygame!

This is my first upload to github.

The intention is to make en easy tweakable simulation of organism floating around search for food or mates to reproduce.

The simulation is somewhat working. 

They eat, and when they eat they get bigger but also slower. this gives starving blobs an advantage.

When they've reached a certain level of food they will try to reproduce.

they need to continously find food.

They also age and can only survive certain amount of ticks.

TODO:
- Right now the new blobs are born at a random location. i whant them to be born at the location of the "mother"

- I would like to se the status(pergnant, seeking partner, starving etc) of the blobs with perhaps different colors or symbols on the blob.

- would be nice i you could pause and click a blob and get status of a certain blob. Maybe even follow in realtime

- Graph showing statistics of a few values. Maybe even in its own window.

- Find out if there is a suitable library like torch or something that could control the movement of the blobs

