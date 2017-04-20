## Solar System Generator
## by Dan R. Paulsen

1. Run the script drp_planetGenerator.py in Maya
2. Run planetGeneratorGUI()
3. To generate a planet, follow the settings on the UI:
a. Name a planet
b. Select radius, number of subdivisions, noise terrain factor, noise terrain height, colour of the planet, rotational speed, inclination of the poles.
c. Moons can be toggled on or off and the number of moons assigned.
d. “Create a Planet!” generates the planet.
e. “Random Planet” randomly assigns the previous values, and generates a planet. The number of moons is still assigned through the checkbox.
f. In order to see the generated planets, the list it should be refreshed via “Refresh Planet List”
4. To generate a solar system with the given planets, follow the settings on the UI:
a. “Orbit Expanse” assigns the radius of the orbit in relation to the last planet size.
b. “Orientation Randomizer” rotates the orbits randomly between 0 and 90 degrees.
c. “Translation Speed“ assigns a value that translates the planets faster.
d. “Size of the Sun” defines the size of the sun.
e. “Let there be light!” button creates the Solar System.
f. “Adjust Camera to Fit All” fits all the objects in the scene on the viewport.
g. “Play the Solar System” starts the animation from frame 0 to 1000.
h. Remember to turn Textured shaded materials on the Viewport.