import os
from pathlib import Path
from datetime import datetime
import PIL.Image
import numpy as np
from ome_types import (to_xml)
from ome_types.model.simple_types import UnitsLength, UnitsTime
from ome_types.model import (OME, Image, Pixels, Instrument, InstrumentRef,
                             Microscope, Objective, Channel, TiffData, Plane)
#from GCI_Data import KeyenceMetadata
import tifffile
import zipfile
import xml.dom.minidom
import glob

#Stitching
import stitch2d

''' This line is needed because large images will return an error of a suspected 
"decompression bomb DOS attack." This maximum image size is arbitrary.'''
PIL.Image.MAX_IMAGE_PIXELS = 10000000000

def Stitch(MainDirectory, GCI_List, Path_List, ImgPath_List, SlideID):
    try: 
        GCI_Path = glob.glob(GCI_List)
        GCI = GCI_Path[0]
        GCI_Zip  = zipfile.ZipFile(GCI, "r")
        def parseProperties(GCI_Zip, zipinfo):
            with GCI_Zip.open(zipinfo) as GCI_info:
                dom = xml.dom.minidom.parse(GCI_info)
            return {node.tagName : node.firstChild.data 
                    if node.firstChild is not None 
                    else None for node in dom.firstChild.childNodes}
        ImageJoint_XML = parseProperties(GCI_Zip, "GroupFileProperty/ImageJoint/properties.xml")
        x_num = ImageJoint_XML['Column']
        
        #Number of cores to use
        #Currently only works with 1 core for some reason
        stitch2d.Mosaic.num_cores = 1
        
        #Settings for Stitching the WSI
        X = stitch2d.create_mosaic(Path_List,
                                  dim = int(x_num),
                                  origin = "upper left",
                                  direction = "horizontal",
                                  pattern = "snake")
        
        #Align the images
        print("Aligning " + SlideID)
        X.align()
        
        #Smooth seems between images
        print("Smoothing Seams...")
        X.smooth_seams()
        
        print("Stitching " + SlideID)
        #Return the stitched image as an array to convert to OME-TIFF
        X_arr = X.stitch()
        #OpenCV, used to stitch/align the images, uses BGR and not RGB when ordering the colors so we need to change the order
        X_arr = X_arr[...,::-1]
        
        #Define the array as "Stitched_Image"
        Stitched_Image = X_arr
        
        #Create the OME-TIFF
        print("Converting " + SlideID + " to OME-TIFF")
        Create_OMETIFF(MainDirectory, GCI_List, ImgPath_List, SlideID, Stitched_Image)

    except:
        print("There was an error! I quit.")
        pass

def Create_OMETIFF(MainDirectory, GCI_List, ImgPath_List, SlideID, Stitched_Image):
    GCI_Path = glob.glob(GCI_List)
    GCI = GCI_Path[0]
    GCI_Zip  = zipfile.ZipFile(GCI, "r")
    def parseProperties(GCI_Zip, zipinfo):
        with GCI_Zip.open(zipinfo) as GCI_info:
            dom = xml.dom.minidom.parse(GCI_info)
            return {node.tagName : node.firstChild.data 
                    if node.firstChild is not None 
                    else None for node in dom.firstChild.childNodes}
    
    Toplevel_XML = parseProperties(GCI_Zip, "GroupFileProperty/properties.xml")
    ImageJoint_XML = parseProperties(GCI_Zip, "GroupFileProperty/ImageJoint/properties.xml")
    Image_XML = parseProperties(GCI_Zip, "GroupFileProperty/Image/properties.xml")

    #Stack Information
    Stack_XML = parseProperties(GCI_Zip, 'GroupFileProperty/Stack/properties.xml')

    #Objective Information
    Lens_XML = parseProperties(GCI_Zip, "GroupFileProperty/Lens/properties.xml")

    #Channel 0 Information
    Channel0_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel0/properties.xml")
    Channel0_CameraSettings_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel0/Shooting/Parameter/properties.xml")
    Channel0_Exposure_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel0/Shooting/Parameter/ExposureTime/properties.xml")
    Channel0_ImageCorrection_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel0/ImageCorrection/properties.xml")
    Channel0_LUT_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel0/ImageCorrection/LookupTable/properties.xml")
    Channel0_Balance_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel0/ImageCorrection/WhiteBalance/properties.xml")
    
    #Channel 1 Information
    Channel1_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel1/properties.xml")
    Channel1_CameraSettings_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel1/Shooting/Parameter/properties.xml")
    Channel1_Exposure_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel1/Shooting/Parameter/ExposureTime/properties.xml")
    Channel1_ImageCorrection_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel1/ImageCorrection/properties.xml")
    Channel1_LUT_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel1/ImageCorrection/LookupTable/properties.xml")
    Channel1_Balance_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel1/ImageCorrection/WhiteBalance/properties.xml")
    
    #Channel 2 Information
    Channel2_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel2/properties.xml")
    Channel2_CameraSettings_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel2/Shooting/Parameter/properties.xml")
    Channel2_Exposure_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel2/Shooting/Parameter/ExposureTime/properties.xml")
    Channel2_ImageCorrection_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel2/ImageCorrection/properties.xml")
    Channel2_LUT_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel2/ImageCorrection/LookupTable/properties.xml")
    Channel2_Balance_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel2/ImageCorrection/WhiteBalance/properties.xml")
    
    #Channel 3 Information
    Channel3_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel3/properties.xml")
    Channel3_CameraSettings_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel3/Shooting/Parameter/properties.xml")
    Channel3_Exposure_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel3/Shooting/Parameter/ExposureTime/properties.xml")
    Channel3_ImageCorrection_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel3/ImageCorrection/properties.xml")
    Channel3_LUT_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel3/ImageCorrection/LookupTable/properties.xml")
    Channel3_Balance_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel3/ImageCorrection/WhiteBalance/properties.xml")
    
    #Channel 4 Information
    Channel4_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel4/properties.xml")
    Channel4_CameraSettings_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel4/Shooting/Parameter/properties.xml")
    Channel4_Exposure_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel4/Shooting/Parameter/ExposureTime/properties.xml")
    Channel4_ImageCorrection_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel4/ImageCorrection/properties.xml")
    Channel4_LUT_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel4/ImageCorrection/LookupTable/properties.xml")
    Channel4_Balance_XML = parseProperties(GCI_Zip, "GroupFileProperty/Channel4/ImageCorrection/WhiteBalance/properties.xml")
    
    
    #Number of Tiles in the X and Y Direction
    x_num = ImageJoint_XML['Column']
    y_num = ImageJoint_XML['Row']

    #Number of Z-sections and Pitch
    z_num = Stack_XML['TotalNumber']
    z_pitch = int(Stack_XML['Pitch'])/10

    #Objective Information
    Objective_Mag = Lens_XML['Magnification']
    
    #Channel 1
    Channel0_Status = Channel0_XML['IsShot'] # True = ON, False = OFF
    Ch0_Exposure = int(Channel0_Exposure_XML['Numerator'])/int(Channel0_Exposure_XML['Denominator'])
    FilterCube0 = Channel0_XML['Comment']
    
    #Channel 2
    Channel1_Status = Channel1_XML['IsShot'] # True = ON, False = OFF
    Ch1_Exposure = int(Channel1_Exposure_XML['Numerator'])/int(Channel1_Exposure_XML['Denominator'])
    FilterCube1 = Channel1_XML['Comment']
    
    #Channel 3
    Channel2_Status = Channel2_XML['IsShot'] # True = ON, False = OFF
    Ch2_Exposure = int(Channel2_Exposure_XML['Numerator'])/int(Channel2_Exposure_XML['Denominator'])
    FilterCube2 = Channel2_XML['Comment']
    
    #Channel 4
    Channel3_Status = Channel3_XML['IsShot'] # True = ON, False = OFF
    Ch3_Exposure = int(Channel3_Exposure_XML['Numerator'])/int(Channel3_Exposure_XML['Denominator'])
    FilterCube3 = Channel3_XML['Comment']
    
    '''Channel 5 is reserved for the RGB composite that the microscope generates and is not
    relevant for our use'''


    ImgPath = ImgPath_List

    Objective_Mag = Lens_XML['Magnification']
    Binning_Settings = str(Channel3_CameraSettings_XML['Binnin'])


    '''Converting the image to a numpy array, then defining the image size in 
    X and Y in addition to defining the number of channels in the image'''
    ImgArray = np.array(Stitched_Image)
    #Number of pixels in the Y direction
    Image_Y = int(ImgArray.shape[0])
    #Number of pixels in the X direction
    Image_X = int(ImgArray.shape[1])
    #Number of channels in the image (eg. RGB has 3, 1 for each color)
    Image_C = int(ImgArray.shape[2])
    
    '''The date and time the GCI file was created in UTC. This will become 
    the aquisition date/time'''
    ImageTimestamp = os.path.getmtime(GCI)
    ImageTimeUTC = datetime.utcfromtimestamp(ImageTimestamp)
    
    #Return the original TIFF name so we can use this to name the OME-TIFF
    ImgName = Path(ImgPath).stem
    
    #Create a blank OME-XML
    ome = OME()
    
    Keyence_Microscope = Microscope(
        manufacturer = 'Keyence Corportation',
        model = 'BZ-X800',
        type = 'Inverted')
    
    #Objective Information
    Objective_4X = Objective(
        id = 'Objective:1',
        manufacturer = 'Keyence Corporation', #This will not change
        model = '4X PlanFluor',
        nominal_magnification = 4,
        working_distance = 16.5,
        working_distance_unit = 'mm',
        lens_na = 0.13,
        immersion = 'Air')
    
    Objective_10X = Objective(
        id = 'Objective:2',
        manufacturer = 'Keyence Corporation', #This will not change
        model = '10X PlanFluor',
        nominal_magnification = 10,
        working_distance = 14.5,
        working_distance_unit = 'mm',
        lens_na = 0.45,
        immersion = 'Air')
    
    Objective_20X = Objective(
        id = 'Objective:3',
        manufacturer = 'Keyence Corporation', #This will not change
        model = '20X PlanApo',
        nominal_magnification = 20,
        working_distance = 0.6,
        working_distance_unit = 'mm',
        lens_na = 0.75,
        immersion = 'Air')
    
    Objective_40X = Objective(
        id = 'Objective:4',
        manufacturer = 'Keyence Corporation', #This will not change
        model = '40X PlanApo',
        nominal_magnification = 40,
        working_distance = 0.95,
        working_distance_unit = 'mm',
        lens_na = 0.75,
        immersion = 'Air')
    
    Objective_100X = Objective(
        id = 'Objective:5',
        manufacturer = 'Keyence Corporation', #This will not change
        model = '100X PlanApo',
        nominal_magnification = 100,
        working_distance = 0.13,
        working_distance_unit = 'mm',
        lens_na = 1.45,
        immersion = 'Oil')
    
    Objective_X = Objective()
    
    #Setting correct objective in OME-XML and defining image pixel size
    def SelectObjective(Objective_Mag, Objective_4X , Objective_10X, Objective_20X,
                        Objective_40X, Objective_100X, Objective_X):   
        if Objective_Mag == 400:
            ImgObjective = Objective_4X
            PixelSizeX = 1.8907
            PixelSizeY = 1.8907
        elif Objective_Mag == 1000:
            ImgObjective = Objective_10X
            PixelSizeX = 0.7562
            PixelSizeY = 0.7562            
        elif Objective_Mag == 2000:
            ImgObjective = Objective_20X
            PixelSizeX = 0.3784
            PixelSizeY = 0.3784
        elif Objective_Mag == 4000:
            ImgObjective = Objective_40X
            PixelSizeX = 0.1891
            PixelSizeY = 0.1891
        elif Objective_Mag == 10000:
            ImgObjective = Objective_100X
            PixelSizeX = 0.0756
            PixelSizeY = 0.0756
        else:
            ImgObjective = Objective_X
            PixelSizeX = 1
            PixelSizeY = 1
            print("Unable to find the objective used, setting a blank objective and a pixel size of 1 in both the X and Y directions.")
        return ImgObjective, PixelSizeX, PixelSizeY

#Setting the correct binning to adjust the X and Y pixel size
    def Binning(Binning_Settings):
        if Binning_Settings == "Off":
            BinSize = 1
        elif Binning_Settings == "TwoByTwo":
            BinSize = 4
        elif Binning_Settings == "ThreeByThree":
            BinSize = 9 
        elif Binning_Settings == "FourByFour":
            BinSize = 16
        elif Binning_Settings == "EightByEight":
            BinSize = 64
        elif Binning_Settings == "TwelveByTwelve":
            BinSize = 144
        else:
            BinSize = 1
            print("Unable to determine if binning was used, assuming none.")
        return BinSize

    def ColorModeCH4(FilterCube3):
        if FilterCube3 == "Brightfield":
            ColorDef = 'rgb'
        else:
            ColorDef = "minisblack"
        return ColorDef

    BinSize = Binning(Binning_Settings)
    ImgObjective, PixelSizeX, PixelSizeY = SelectObjective(int(Objective_Mag), Objective_4X,
                                                           Objective_10X, Objective_20X,
                                                           Objective_40X, Objective_100X,
                                                           Objective_X)

    Instrument_Config = Instrument(
        id = 'Instrument:1',
        microscope = Keyence_Microscope,
        objectives = [ImgObjective])

    Channel_Config = Channel(
        illumination_type = 'Transmitted',
        contrast_method = 'Brightfield',
        samples_per_pixel = Image_C)
    
    Plane_Config = Plane(
        the_c = 0,
        the_t = 0,
        the_z = 0,
        delta_t = 0,
        exposure_time = Ch3_Exposure,
        exposure_time_unit = UnitsTime.SECOND)

    Tiff_Config = TiffData(first_c = 1, 
                           first_t = 1, 
                           first_z = 1, 
                           ifd = 0, 
                           plane_count = 1)

    Image_Data = Image(
        name = ImgName,
        acquisition_date = ImageTimeUTC,
        pixels = Pixels(
            dimension_order = 'XYCZT',
            size_c = Image_C,
            size_t = 1,
            size_x = Image_X,
            size_y = Image_Y,
            size_z = 1,
            type = 'uint8', #8-bit RGB images for brightfield, 8/14-bit monochrome
            channels = [Channel_Config],
            physical_size_x = PixelSizeX * BinSize,
            physical_size_x_unit = UnitsLength.MICROMETER,
            physical_size_y = PixelSizeY * BinSize,
            physical_size_y_unit = UnitsLength.MICROMETER,
            planes = [Plane_Config],
            tiff_data_blocks = [Tiff_Config]))

    ome.instruments.append(Instrument_Config)
    ome.images.append(Image_Data)
    ome.images[0].instrument_ref = InstrumentRef(Instrument_Config.id)
    Final_OMEXML = to_xml(ome)

    save_path_file = "OME_XML.xml"
    with open(save_path_file, "w") as f:
        f.write(Final_OMEXML)
        
    #Write the OME-TIFF
    tifffile.imsave(MainDirectory + '/' + SlideID + '.ome.tif', Stitched_Image, photometric = 'rgb', 
                     compression='deflate', description = Final_OMEXML,
                     metadata = None)