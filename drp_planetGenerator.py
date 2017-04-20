##
### CAP Scripting - Assessed Mini-Project
### Solar System Generator
### by Daniel Rosas Paulsen
##

import maya.cmds as mc
import random as random

mc.file(new = True, force = True)

# List of global variables

planetsList = []
planetSize = []
moonList = []
moonListSize = []
moonGrpList = []

## UI Variables
planetNameTXT,radiusFSG,subdivFSG,noiseFSG,noiseAmpFSG,colourCSG,rotationalFSG,inclinationFSG = None,None,None,None,None,None,None,None
moonBoolCBX =[]
numberMoonsISG=[]
planetGeneratorBTN,planetRandomBTN,planetTSL,planetRefreshBTN,orbitExpanseFSG,orientationRandFSG,transSpeedFSG,sunSizeFSG,solarSystemGeneratorBTN,playbackBTN,cameraBTN=None,None,None,None,None,None,None,None,None,None,None

##-----------------------------------------------------------------------------
# UI Definition
##-----------------------------------------------------------------------------

def planetGeneratorGUI():
    global planetNameTXT,radiusFSG,subdivFSG,noiseFSG,noiseAmpFSG,colourCSG,rotationalFSG,inclinationFSG,planetTSL,orbitExpanseFSG,orientationRandFSG,transSpeedFSG,sunSizeFSG,moonBoolCBX,numberMoonsISG
    
     # if the planetGenerator window exists, delete it    
    if (mc.window("planetUI",exists=True)):
        mc.deleteUI("planetUI")

    # Define window properties 
    planetWindow = mc.window("planetUI", mxb=False, mnb=False, title="Planet Generator!")

    # layout of the ui
    mc.columnLayout("mainColumn",adj=True,cw=200,cal="left")
    mc.text(label="1. Start with a planet")
    mc.separator(style="single")

    # name your planet 
    mc.text(label="Planet Name")
    planetNameTXT = mc.textField()

    # set de customization parameters
    mc.text(label="Customize your Planet")
    radiusFSG = mc.floatSliderGrp(label="Radius",minValue=1, maxValue=50, value=10, field=True)
    subdivFSG = mc.floatSliderGrp(label="Subdivisions",minValue=10, maxValue=200, value=50, field=True)
    noiseFSG = mc.floatSliderGrp(label="Terrain Unease",minValue=1, maxValue=50, value=25, field=True)
    noiseAmpFSG = mc.floatSliderGrp(label="Terrain Height",minValue=0, maxValue=1, value=1, field=True)
    colourCSG = mc.colorSliderGrp(label="Colour", rgb = (1,0,0))
    rotationalFSG = mc.floatSliderGrp(label="Rotational Speed",minValue=1, maxValue=10, value=1, field=True)
    inclinationFSG = mc.floatSliderGrp(label="Inclination",minValue=0, maxValue=90, value=10, field=True)

    # Moon Generator
    moonBoolCBX = mc.checkBox(label="Has the planet moons?")
    numberMoonsISG = mc.intSliderGrp(label="Number of Moons",minValue=0, maxValue=5, value=1, field=True)
    
    # Planet Generator Buttons 
    planetGeneratorBTN = mc.button("Create a Planet!", command = "getUIvalues()")
    planetRandomBTN = mc.button("Random Planet", command = "createRandomPlanet()")

    #### Solar System

    mc.text(label="2. Refresh to see your planets")
    mc.separator(style="single")

    planetTSL = mc.textScrollList(height=150)
    planetRefreshBTN = mc.button("Refresh Planet List", command = "refreshPlanetsTSL()")
    
    ## Solar System values
    orbitExpanseFSG = mc.floatSliderGrp(label="Orbit Expanse",minValue=1, maxValue=10, value=5, field=True)
    orientationRandFSG = mc.floatSliderGrp(label="Orientation Randomizer",minValue=1, maxValue=10, value=5, field=True)
    transSpeedFSG = mc.floatSliderGrp(label="Translation Speed",minValue=0.1, maxValue=10, value=1, field=True)
    sunSizeFSG = mc.floatSliderGrp(label="Size of the Sun",minValue=50, maxValue=100, value=50, field=True)

    # Solar System Buttons
    mc.text(label="3. Create a Solar System")
    mc.separator(style="single")

    solarSystemGeneratorBTN = mc.button("Let there be light!", command = "createSolarSystem()")
    cameraBTN = mc.button("Adjust Camera to Fit All", command = "cameraAdjust()")
    playbackBTN = mc.button("Play the Solar System", command = "playSolarSystem()")
    #startAgainBTN = mc.button("Start Again?", command = "startNew()")

    mc.showWindow(planetWindow)

##-----------------------------------------------------------------------------
# Function to get the UI values and run the Planet Generator
##-----------------------------------------------------------------------------

def getUIvalues():
    global planetNameTXT,radiusFSG,subdivFSG,noiseFSG,noiseAmpFSG,colourCSG,rotationalFSG,inclinationFSG,moonBoolCBX,numberMoonsISG
   
    # Query all Planet attributes
    planetName = mc.textField(planetNameTXT,query=True,text=True)
    planetRadius = mc.floatSliderGrp(radiusFSG,query=True, value=True)
    subdivX = mc.floatSliderGrp(subdivFSG,query=True, value=True)
    subdivY = mc.floatSliderGrp(subdivFSG,query=True, value=True)    
    freqNoise = mc.floatSliderGrp(noiseFSG,query=True, value=True)
    amplitudeNoise = mc.floatSliderGrp(noiseAmpFSG,query=True, value=True)
    planetRGB = mc.colorSliderGrp(colourCSG,query=True,rgbValue=True)
    rotSpeed = mc.floatSliderGrp(rotationalFSG,query=True, value=True)
    inclination = mc.floatSliderGrp(inclinationFSG,query=True, value=True)
    
    print planetName, planetRadius, subdivX, subdivY, freqNoise, amplitudeNoise, planetRGB, rotSpeed, inclination
    createPlanetBase(planetRadius,subdivX,subdivY,planetName,freqNoise,amplitudeNoise,planetRGB,rotSpeed,inclination)

##-----------------------------------------------------------------------------
# Function to create a random planet 
##-----------------------------------------------------------------------------

def createRandomPlanet():
    
    planetName = ("randomPlanet"+str(random.randint(0,999)))
    planetRadius = random.uniform(0,30)
    subdivX = random.uniform(20,60)
    subdivY = random.uniform(20,60)
    freqNoise = random.uniform(20,50)
    amplitudeNoise = random.uniform(0.1,1)
    planetRGB = [random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
    rotSpeed = random.uniform(1,10)
    inclination = random.uniform(0,45)
    
    createPlanetBase(planetRadius,subdivX,subdivY,planetName,freqNoise,amplitudeNoise,planetRGB,rotSpeed,inclination)
    

##-----------------------------------------------------------------------------
# Function to get Solar System values and run the Solar System Generator
##-----------------------------------------------------------------------------

def createSolarSystem():
    global orbitExpanseFSG,orientationRandFSG,transSpeedFSG,sunSizeFSG,planetSize,planetsList

    orbitExpanse = mc.floatSliderGrp(orbitExpanseFSG,query=True, value=True)
    orientationRandom = mc.floatSliderGrp(orientationRandFSG,query=True, value=True)
    translationSpeed = mc.floatSliderGrp(transSpeedFSG,query=True, value=True)
    sunSize = mc.floatSliderGrp(sunSizeFSG,query=True, value=True)
        
    # Index values for list reading
    i = 0
    j = 0
        
    # Empty list for scale values from all the planets in the list
    planetScalable = []
    
    # Save all the scale values of the planets to calculate the orbit size    
    for eachScalablePlanet in planetSize:
        planetScalable.append(mc.getAttr(eachScalablePlanet[0]+".scaleX"))
        

    for eachPlanet in planetsList:
        orbitPath = [1,100] # initial number of frames for the animation
        
        # First Planet Value
        #planetScale = mc.getAttr(eachPlanet[0]+".scaleX")
        firstPlanetValue = sunSize + (planetScalable[j]*2)
        
        # Calculate the speed of the planet through the end frame of the motion path animator
        planetEndFrame = int(orbitPath[1])*(planetScalable[j]/translationSpeed)
        
        # Group the planet to keep the rotation in the object, and connect the group to the motion path
        planetGroup = mc.group(eachPlanet,a=True,name=(eachPlanet[0]+"_grp"),w=True)
        
        # Orbit inclination random number
        eachOrbitRandom = (random.uniform(0,orientationRandom))*orientationRandom
        
        # Create the planet orbit with the previous values
        planetOrbit = mc.circle(n=(eachPlanet[0]+"_orbit"),c=[0,0,0],nr=[0,1,0],sw=360,r=(firstPlanetValue + i),d=3,ch=True)
        mc.rotate(eachOrbitRandom,eachOrbitRandom,0,planetOrbit)
        
        # Connect the planet group to the orbit through a motion path
        planetPathAnimation = mc.pathAnimation(planetGroup,planetOrbit[0],fractionMode=True,follow=True,followAxis="z",upAxis="y",worldUpType="vector",worldUpVector=[0,1,0],inverseUp=False,inverseFront=False,bank=False,startTimeU=1,endTimeU=planetEndFrame,name=(eachPlanet[0]+"_orbit_motionPath"))

        # Modification of the keyframes, key selection, linear tangents and infitinty to cycle
        mc.selectKey(planetPathAnimation,add=True,k=True,at="uValue")
        mc.keyTangent(planetPathAnimation,at="uValue",itt="linear",ott="linear")
        mc.setInfinity(at=(planetPathAnimation+".uValue"),poi="cycle")

        # Assign a higher value for the radius of the orbit
        i+=(planetScalable[j]*orbitExpanse*2)
        j = (j+1) % len(planetsList)
            
            
    # Create the sun, based on the planet function        
    createPlanetBase(sunSize,50,50,"theSun",25,1,[1,1,0],2,0)

##-----------------------------------------------------------------------------
# Moon Checker if True or False 
##-----------------------------------------------------------------------------

def moonChecker():
    global moonBoolCBX
    if (mc.checkBox(moonBoolCBX,query=True, value=True)):
        return True
    else:
        return False

##-----------------------------------------------------------------------------
# Moon Generator: values. To assign random values for each moon
##-----------------------------------------------------------------------------

def moonGenerator():
    global numberMoonsISG
    numberMoons = mc.intSliderGrp(numberMoonsISG,query=True, value=True)
    
    for x in range(numberMoons):
        moonName = ("randomMoon"+str(random.randint(0,999)))
        moonRadius = random.uniform(0,3)
        moonNoise = random.uniform(10,50)
        moonRGB = [random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
        rotSpeed = random.uniform(1,5)
        inclination = random.uniform(0,90)
        createMoonBase(moonRadius,10,10,moonName,moonNoise,1,moonRGB,rotSpeed,inclination)
        
##-----------------------------------------------------------------------------
# Moon Generator: mesh, based on the planet generator
##-----------------------------------------------------------------------------
        
def createMoonBase(planetRadius,subdivX,subdivY,planetName,freqNoise,amplitudeNoise,planetRGB,rotSpeed,inclination):
    global planetSize,planetsList,moonBoolCBX,numberMoonsISG,moonList
    
    # create base sphere
    planet = mc.polySphere(n=planetName,r=1,sx=subdivX,sy=subdivY,ax=[0,1,0],cuv=2,ch=1)
    mc.rotate(0,0,inclination, relative = True)
    mc.scale(planetRadius,planetRadius,planetRadius, r=True)
    
    # create texture deformer
    planetDeformer = mc.textureDeformer(planet,envelope=1,strength=1,offset=0,vectorStrength=[1, 1, 1],vectorOffset=[0, 0, 0],vectorSpace="Object",direction="Normal",pointSpace="UV",exclusive="",name=(planetName+"_txtrDeformer"))

    # create noise node and connect attributes to textureDeformer
    planetNoise = mc.shadingNode("noise", asTexture=True,name=(planetName+"_noise"))
    planetNoise2DTexture = mc.shadingNode("place2dTexture", asUtility=True,name=(planetName+"_place2dTxtr"))

    mc.connectAttr((planetNoise2DTexture + ".outUV"),(planetNoise + ".uv"))
    mc.connectAttr((planetNoise2DTexture + ".outUvFilterSize"),( planetNoise + ".uvFilterSize"))

    mc.connectAttr((planetNoise + ".outColor"), (planetDeformer[0] + ".texture"), force = True)
    mc.setAttr((planetNoise + ".frequency"),freqNoise)
    mc.setAttr((planetNoise + ".amplitude"),amplitudeNoise)
    mc.setAttr((planetNoise + ".sizeRand"),1)

    # create surface shader for planet
    planetShader = mc.shadingNode("surfaceShader",asShader=True,name=(planetName+"surfaceShdr"))
    planetSG = mc.sets(renderable=True,noSurfaceShader=True, empty=True, name=(planetName+"_SG"))
    
    mc.connectAttr((planetShader + ".outColor"),(planetSG + ".surfaceShader"),force = True)
    mc.select(planet)
    mc.hyperShade(assign=planetShader)

    # create 2d ramp to assign a colour to the planet
    planetRamp = mc.shadingNode("ramp",asTexture=True, name=(planetName+"_ramp"))
    planetRamp2DTexture = mc.shadingNode("place2dTexture", asUtility=True, name = (planetName+"_ramp_2dTxtr"))
    mc.connectAttr((planetRamp2DTexture +".outUV"), (planetRamp + ".uv"))
    mc.connectAttr((planetRamp2DTexture + ".outUvFilterSize"), (planetRamp2DTexture + ".uvFilterSize"))
    mc.connectAttr((planetRamp +".outColor"),(planetShader +".outColor"),force=True)
   
    # ramp attributes modifier for colours, poles are white
    mc.setAttr((planetRamp +".colorEntryList[0].position"), 0)
    mc.setAttr((planetRamp +".colorEntryList[0].color"),1,1,1, type="double3" )

    mc.setAttr((planetRamp +".colorEntryList[1].position"), 0.2)
    mc.setAttr((planetRamp +".colorEntryList[1].color"),planetRGB[0],planetRGB[1],planetRGB[2], type="double3" )

    mc.setAttr((planetRamp +".colorEntryList[2].position"), 0.8)
    mc.setAttr((planetRamp +".colorEntryList[2].color"),planetRGB[0],planetRGB[1],planetRGB[2], type="double3" )

    mc.setAttr((planetRamp +".colorEntryList[3].position"), 1)
    mc.setAttr((planetRamp +".colorEntryList[3].color"),1,1,1, type="double3" )

    mc.setAttr((planetRamp +".interpolation"), 6)
        
    # Delete the history of the planet node
    mc.delete(planet, ch=True)
    
    MoonTransformGrp = mc.ls(planet)
    mc.rotate(0,0,inclination, MoonTransformGrp, relative = True)
        
    moonList.append(MoonTransformGrp)
    
    # Create expression for planet rotation
    planetExpression = mc.expression(s=((str(MoonTransformGrp[0]))+".rotateY = ((time*10)*" +(str(rotSpeed))+")" ),o=MoonTransformGrp[0],ae=True,uc="all" )    

##-----------------------------------------------------------------------------
# Moon Generator: Mini Solar System for each moon orbiting the planet
##-----------------------------------------------------------------------------

def moonMiniSolarSystem(COGScale):
    global moonListSize, moonList, moonGrpList

    i = 0

    for eachPlanet in moonList:        
        orbitPath = [1,100] # initial number of frames for the animation
        
        # First Planet Value
        moonScale = mc.getAttr(eachPlanet[0]+".scaleX")
        firstPlanetValue = COGScale + (COGScale*0.5)
        
        # Calculate the speed of the planet through the end frame of the motion path animator
        planetEndFrame = int(orbitPath[1])*(moonScale*2)
        
        # Group the planet to keep the rotation in the object, and connect the group to the motion path
        moonGroup = mc.group(eachPlanet,a=True,name=(eachPlanet[0]+"_grp"),w=True)
        
        # Orbit inclination random number
        eachOrbitRandom = (random.uniform(0,10))
        
        # Create the planet orbit with the previous values
        planetOrbit = mc.circle(n=(eachPlanet[0]+"_orbit"),c=[0,0,0],nr=[0,1,0],sw=360,r=(firstPlanetValue + i),d=3,ch=True)
        mc.rotate(eachOrbitRandom,eachOrbitRandom,0,planetOrbit)
        
        # Connect the planet group to the orbit through a motion path
        moonPathAnimation = mc.pathAnimation(moonGroup,planetOrbit,fractionMode=True,follow=True,followAxis="z",upAxis="y",worldUpType="vector",worldUpVector=[0,1,0],inverseUp=False,inverseFront=False,bank=False,startTimeU=1,endTimeU=planetEndFrame, name=(eachPlanet[0]+"_moon_motionPath"))

        # Modification of the keyframes, key selection, linear tangents and infitinty to cycle
        mc.selectKey(moonPathAnimation,add=True,k=True,at="uValue")
        mc.keyTangent(moonPathAnimation,at="uValue",itt="linear",ott="linear")
        mc.setInfinity(at=(moonPathAnimation+".uValue"),poi="cycle")

        moonIndex = mc.group(planetOrbit,name=(eachPlanet[0]+"_orbitMoonGrp"))
        
        moonGrpList.append(moonIndex)
        
        i+=(moonScale*2)

   
##-----------------------------------------------------------------------------
# Planet Generator
##-----------------------------------------------------------------------------

def createPlanetBase(planetRadius,subdivX,subdivY,planetName,freqNoise,amplitudeNoise,planetRGB,rotSpeed,inclination):
    global planetSize, planetsList,moonBoolCBX,numberMoonsISG,moonList,moonGrpList
    # create base sphere
    planet = mc.polySphere(n=(planetName+"_base"),r=1,sx=subdivX,sy=subdivY,ax=[0,1,0],cuv=2,ch=1)
    mc.rotate(0,0,inclination, relative = True)
    mc.scale(planetRadius,planetRadius,planetRadius, r=True)
    
    # create texture deformer
    planetDeformer = mc.textureDeformer(planet,envelope=1,strength=1,offset=0,vectorStrength=[1, 1, 1],vectorOffset=[0, 0, 0],vectorSpace="Object",direction="Normal",pointSpace="UV",exclusive="",name=(planetName+"_txtrDeformer"))

    # create noise node and connect attributes to textureDeformer
    planetNoise = mc.shadingNode("noise", asTexture=True,name=(planetName+"_noise"))
    planetNoise2DTexture = mc.shadingNode("place2dTexture", asUtility=True,name=(planetName+"_place2dTxtr"))

    mc.connectAttr((planetNoise2DTexture + ".outUV"),(planetNoise + ".uv"))
    mc.connectAttr((planetNoise2DTexture + ".outUvFilterSize"),( planetNoise + ".uvFilterSize"))

    mc.connectAttr((planetNoise + ".outColor"), (planetDeformer[0] + ".texture"), force = True)
    mc.setAttr((planetNoise + ".frequency"),freqNoise)
    mc.setAttr((planetNoise + ".amplitude"),amplitudeNoise)
    mc.setAttr((planetNoise + ".sizeRand"),1)

    # create surface shader for planet
    planetShader = mc.shadingNode("surfaceShader",asShader=True,name=(planetName+"surfaceShdr"))
    planetSG = mc.sets(renderable=True,noSurfaceShader=True, empty=True, name=(planetName+"_SG"))
    
    mc.connectAttr((planetShader + ".outColor"),(planetSG + ".surfaceShader"),force = True)
    mc.select(planet)
    mc.hyperShade(assign=planetShader)

    # create 2d ramp to assign a colour to the planet
    planetRamp = mc.shadingNode("ramp",asTexture=True, name=(planetName+"_ramp"))
    planetRamp2DTexture = mc.shadingNode("place2dTexture", asUtility=True, name = (planetName+"_ramp_2dTxtr"))
    mc.connectAttr((planetRamp2DTexture +".outUV"), (planetRamp + ".uv"))
    mc.connectAttr((planetRamp2DTexture + ".outUvFilterSize"), (planetRamp2DTexture + ".uvFilterSize"))
    mc.connectAttr((planetRamp +".outColor"),(planetShader +".outColor"),force=True)

    planetWater = mc.polySphere(n=(planetName+"_water"),r=1,sx=subdivX,sy=subdivY,ax=[0,1,0],cuv=2,ch=1)
    mc.scale((planetRadius+(planetRadius*0.01)),(planetRadius+(planetRadius*0.01)),(planetRadius+(planetRadius*0.01)),planetWater, r=True)
   
    # ramp attributes modifier for colours, poles are white
    mc.setAttr((planetRamp +".colorEntryList[0].position"), 0)
    mc.setAttr((planetRamp +".colorEntryList[0].color"),1,1,1, type="double3" )

    mc.setAttr((planetRamp +".colorEntryList[1].position"), 0.2)
    mc.setAttr((planetRamp +".colorEntryList[1].color"),planetRGB[0],planetRGB[1],planetRGB[2], type="double3" )

    mc.setAttr((planetRamp +".colorEntryList[2].position"), 0.8)
    mc.setAttr((planetRamp +".colorEntryList[2].color"),planetRGB[0],planetRGB[1],planetRGB[2], type="double3" )

    mc.setAttr((planetRamp +".colorEntryList[3].position"), 1)
    mc.setAttr((planetRamp +".colorEntryList[3].color"),1,1,1, type="double3" )

    mc.setAttr((planetRamp +".interpolation"), 6)
        
    # create water levels for planet
    planetWaterShader = mc.shadingNode("surfaceShader",asShader=True,name=(planetName+"_water_surfaceShdr"))
    planetWaterSG = mc.sets(renderable=True,noSurfaceShader=True, empty=True, name=(planetName+"_water_SG"))
    
    mc.setAttr((planetWaterShader + ".outColor"), (planetRGB[0]-(planetRGB[0]*0.5)),(planetRGB[1]-(planetRGB[1]*0.5)),(planetRGB[2]-(planetRGB[2]*0.5)), type="double3")
    mc.connectAttr((planetWaterShader + ".outColor"),(planetWaterSG + ".surfaceShader"),force = True)
    mc.select(planetWater)
    mc.hyperShade(assign=planetWaterShader)
        
    # Delete the history of the planet node
    mc.delete(planet, ch=True)
    mc.delete(planetWater, ch=True)
    
    planetTransform = mc.ls(planet,planetWater)
    mc.rotate(0,0,inclination, planetTransform, relative = True)
    planetGrp = mc.group(planetTransform,name=planetName)
        
    # If a planet is not named as the sun, it runs the moon generator functions and stores them on a list
    if planetName!="theSun":
        if moonChecker():
            moonGenerator()
            moonMiniSolarSystem(planetRadius)
            mc.parent(moonGrpList,planetGrp)
            moonGrpList=[]
            moonList=[]
        
    # selects the transform node of the planet and stores it on a list
    planetTransformGrp = mc.ls(planetGrp)
    planetsList.append(planetTransformGrp)
    
    planetToScale = mc.ls(planet)
    planetSize.append(planetToScale)
    
    # Create expression for planet rotation, based on the input value
    planetExpression = mc.expression(s=((str(planetTransformGrp[0]))+".rotateY = ((time*10)*" +(str(rotSpeed))+")" ),o=planetTransformGrp[0],ae=True,uc="all" )
    
    
##-----------------------------------------------------------------------------
# Planet textScrollList append
##-----------------------------------------------------------------------------

def refreshPlanetsTSL():
    global planetTSL
    # Cleans the textScrollList before adding any new components
    mc.textScrollList(planetTSL,e=True,ra=True)
    for eachPlanet in planetsList:
        mc.textScrollList(planetTSL, e=True, append = eachPlanet)
            
##-----------------------------------------------------------------------------
# Play the Solar System
##-----------------------------------------------------------------------------

def playSolarSystem():
    mc.playbackOptions(maxTime=1000)
    mc.play(forward=True)
    
##-----------------------------------------------------------------------------
# Adjust the Camera to fit all planets and adjust far clip plane
##-----------------------------------------------------------------------------
    
def cameraAdjust():
    mc.setAttr("perspShape.nearClipPlane", 10)
    mc.viewFit("persp", allObjects=True)
