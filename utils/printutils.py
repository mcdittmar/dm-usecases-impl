# -----------------------------------------------------------------------------
# Print Utilities:
#   * basically toString() methods for the different classes
# -----------------------------------------------------------------------------
from rama.models.mango import Source, VOModelInstance, AssociatedMangoInstance, WebEndpoint
from rama.models.mango import LonLatSkyPosition, Photometry, HardnessRatio, Flag
from rama.models.cube  import SparseCube
from rama.models.measurements import Time, GenericMeasure, Position, ProperMotion
from astropy.time import Time as AstroTime

def get_type_name( obj ):
    result = '.'.join( (obj.__class__.__module__, obj.__class__.__name__) )
    return result
    
def cube_toString( cube, data=True ):
    """
    proxy for cube:SparseCube.toString()
    """
    indent = "    "
    result  = "{}:  \n".format(get_type_name(cube))
    result += "  o Independent Axis: {}  \n".format(str(cube.data[0].independent))
    result += "  o Dependent Axis: {}  \n".format(str(cube.data[0].dependent))
    result += "  o Length: {}  \n".format(len(cube.data))

    if data:
        axis1 = cube.data[0].independent[0]
        for ii in range(len(cube.data)):
            if cube.data[ii] is not None:
                result += "  o    {}".format(measure_toString(cube.data[ii][axis1]._axis.measure))
                for axis in cube.data[0].dependent:
                    result += "      {}".format(measure_toString(cube.data[ii][axis]._axis.measure))
                result += "  \n"

    return result

def source_toString( source ):
    """
    proxy for mango:Source.toString()
    """
    indent = "    "
    result  = "{}:\n".format(get_type_name(source))
    result += "  o identifier: {}\n".format(str(source.identifier))
    result += "  o Associated Parameters:\n"
    if source.parameter_dock is None:
        result += "     0. none\n"
    else:
        n = 0
        for prop in source.parameter_dock:
            n += 1
            result += indent + "{:2d}.".format(n) + property_toString(prop).replace("\n ", "\n"+indent*2 )

    result += "  o Associated Data:\n"
    if source.associated_data_dock is None:
        result += "     0. none\n"
    else:
        n = 0
        for item in (source.associated_data_dock):
            if item is not None:
                n += 1
                # form a_d_d string
                tmpstr  = "{}:\n".format(get_type_name(item))
                tmpstr += "  o semantic: {}\n".format("None" if item.semantic is None else item.semantic.label)
                tmpstr += "  o datatype: {}\n".format(item.data_type)

                if isinstance( item, AssociatedMangoInstance ):
                    tmpstr += "  o mangoInstance:\n"
                    detection = item.mango_instance
                    tmpstr += indent + source_toString( detection ).replace("\n ", "\n"+indent*2 )
                elif isinstance( item, VOModelInstance ):
                    tmpstr += "  o ivoid: {}\n".format(item.ivoid)
                    tmpstr += "  o modelName: {}\n".format(item.model_name)
                    tmpstr += "  o modelURL: {}\n".format(item.model_url)
                    tmpstr += "  o modelInstance:\n"
                    instance = item.model_instance
                    if isinstance( instance, SparseCube ):
                        tmpstr += indent + cube_toString( instance ).replace("\n ", "\n"+indent*2 )
                    else:
                        raise(TypeError("Unrecognized VOModelInstance type ({})\n".format( get_type_name(instance) )))
                elif isinstance( item, WebEndpoint ):
                    tmpstr += "  o contentType: {}\n".format(item.content_type)
                    tmpstr += "  o url: {}\n".format(item.url)
                    
                else:
                    raise(TypeError("Unrecognized AssociatedData type ({})\n".format( get_type_name(item) )))

                result += indent + "{:2d}.".format(n) + tmpstr.replace("\n ", "\n"+indent*2 )
        if n == 0:
            result += "     0. none\n"


    return result

def property_toString( prop ):
    """
    proxy for mango:Parameter.toString()
    """
    result  = "{}:\n".format(get_type_name(prop))
    result += "  o semantic: {}\n".format("None" if prop.semantic is None else prop.semantic.label)
    result += "  o ucd: {}\n".format(prop.ucd)
    result += "  o measure: {}\n".format(measure_toString(prop.measure))
    
    return result

def measure_toString( measure ):
    """
    proxy for meas:Measure.toString()

    Note: some of the types are currently in the Mango model
          but are supported under this method.
    """
    if isinstance( measure, Position ) or isinstance( measure, LonLatSkyPosition ):
        result = position_toString( measure )
    elif isinstance( measure, Time ):
        result = time_toString( measure )
    elif isinstance( measure, ProperMotion ):
        result = propermotion_toString( measure )
    elif isinstance( measure, Photometry ):
        result = photometry_toString( measure )
    elif isinstance( measure, HardnessRatio ):
        result = hardnessratio_toString( measure )
    elif isinstance( measure, GenericMeasure ):
        result = generic_toString( measure )
    elif isinstance( measure, Flag ):
        result = flag_toString( measure )
    else:
        raise(TypeError("Unsupported Measure type ({})".format(str(type(measure)))))
        
    return result

def position_toString( measure ):
    """
    proxy for meas:Position.toString()
    """
    posfmt_2d = "Position: ( {:10.6f} [{}], {:10.6f} [{}] )"
    posfmt_3d = "Position: ( {:10.6f} [{}], {:10.6f} [{}], {:10.6f} [{}] )"
    frame = ""
    
    if ( hasattr( measure.coord, "axis1" ) ): #Point
        frame = measure.coord.coord_sys.frame.space_ref_frame
        if ( measure.coord.axis3 is None ):
            coordstr = posfmt_2d.format( measure.coord.axis1.cval, measure.coord.axis1.unit,
                                         measure.coord.axis2.cval, measure.coord.axis2.unit )
        else:
            coordstr = posfmt_3d.format( measure.coord.axis1.cval, measure.coord.axis1.unit,
                                         measure.coord.axis2.cval, measure.coord.axis2.unit,
                                         measure.coord.axis3.cval, measure.coord.axis3.unit)
    elif ( hasattr( measure.coord, "longitude" ) ): #LonLatSky
        frame = measure.coord.coord_sys.frame.space_ref_frame
        coordstr = posfmt_2d.format( measure.coord.longitude.value, measure.coord.longitude.unit,
                                     measure.coord.latitude.value, measure.coord.latitude.unit)
    elif ( hasattr( measure.coord, "representation_type" ) and hasattr( measure.coord, "frame" ) ): #SkyCoord
        frame = measure.coord.frame.name.upper()
        if ( frame == "GALACTIC" ):
            coordstr = posfmt_2d.format( measure.coord.l.value, measure.coord.l.unit,
                                         measure.coord.b.value, measure.coord.l.unit)
        elif ( frame in ["ICRS","FK5"] ):
            coordstr = posfmt_2d.format( measure.coord.ra.value, measure.coord.ra.unit,
                                         measure.coord.dec.value, measure.coord.dec.unit)
        else:
            raise(TypeError("Unrecognized SkyCoord frame type ({})".format(measure.coord.frame.name)))
    else:
        raise(TypeError("Unsupported Positions type ({})".format(str(type(measure.coord)))))

    errstr = ""
    if measure.error is not None:
        errstr = " " + error_toString( measure.error.stat_error )

    # Add frame 
    result = coordstr + errstr + " [{}]".format(frame)

    return result

def propermotion_toString( measure ):
    """
    proxy for meas:ProperMotion.toString()
    """
    pmfmt = "Proper Motion: ( {:10.6f} [{}], {:10.6f} [{}] )"
    frame = ""
    
    frame = measure.lon.coord_sys.frame.space_ref_frame
    coordstr = pmfmt.format( measure.lon.cval.value, measure.lon.cval.unit,
                             measure.lat.cval.value, measure.lat.cval.unit )

    errstr = ""
    if measure.error is not None:
        errstr = " " + error_toString( measure.error.stat_error )

    # Add frame 
    result = coordstr + errstr + " [{}]".format(frame)

    return result

def time_toString( measure ):
    """
    proxy for meas:Time.toString()
    """
    timefmt = "Time: {:.6f}"
    datetimefmt = "Time: {:s}"

    if ( hasattr( measure.coord, "format")):  #AstroPy Time
        scale = measure.coord.scale.upper()
        if measure.coord.format in ['iso', 'isot', 'fits' ]:
            coordstr = datetimefmt.format(str(measure.coord))
        elif measure.coord.format in ['mjd']:
            coordstr = timefmt.format( measure.coord.mjd )
        else:
            raise(TypeError("Unsupported AstroPy Time type ({})".format(str(type(measure.coord)))))
    #elif ( hasattr( measure.coord, "date" ) ): #MJD,JD,ISOTime
    #    scale = measure.coord.scale.upper()
    #    coordstr = timefmt.format( measure.coord.mjd)
    #elif ( hasattr( measure.coord, "time" ) ): #TimeOffset
    #    scale = measure.coord.scale.upper()
    #    coordstr = timefmt.format( measure.coord.iso)
    else:
        raise(TypeError("Unsupported Time type ({})".format(str(type(measure.coord)))))

    errstr = ""
    if hasattr(measure,"error") and measure.error is not None:
        errstr = " " + error_toString( measure.error.stat_error )

    # Add Time Scale
    result = coordstr + errstr + " [{}]".format(scale)
    
    return result

def photometry_toString( measure ):
    """
    proxy for mango:Photometry.toString()
    """
    photfmt = "Photometry: ({:.3e} [{}])"
    band = ""

    if ( hasattr( measure.coord, "luminosity" ) ): #Photometry
        band = measure.coord.coord_sys.frame.name
        if ( hasattr( measure.coord.luminosity, "value") ):
            coordstr = photfmt.format( measure.coord.luminosity.value, measure.coord.luminosity.unit )
        else:
            coordstr = photfmt.format( measure.coord.luminosity, measure.coord.luminosity.unit )
    else:
        raise(TypeError("Unsupported Photometry type ({})".format(str(type(measure.coord)))))

    errstr = ""
    if measure.error is not None:
        errstr = " " + error_toString( measure.error.stat_error )

    # Add Band
    result = coordstr + errstr + " [band={}]".format(band)
    
    return result

def generic_toString( measure ):
    """
    proxy for meas:GenericMeasure.toString()
    """
    genericfmt = "GenericMeasure: ( {} {:10.6} [{}] )"
    genericfmt_unitless = "GenericMeasure: ( {} {:10.6e} )"

    ucdstr = ""
    if ( hasattr( measure, "ucd" ) ):
        ucdstr = "ucd={}".format(measure.ucd)

    if ( hasattr( measure.coord, "cval" ) ):
        if ( hasattr( measure.coord.cval, "value" ) ): #Quantity
            coordstr = genericfmt.format( ucdstr, measure.coord.cval.value,  measure.coord.cval.unit )
        else:
            coordstr = genericfmt_unitless.format( ucdstr, measure.coord.cval )
    else:
        raise(TypeError("Unsupported GenericMeasure type ({})".format(str(type(measure.coord)))))

    errstr = ""
    if measure.error is not None:
        errstr = " " + error_toString( measure.error.stat_error )

    result = coordstr + errstr
    
    return result

def hardnessratio_toString( measure ):
    """
    proxy for mango:HardnessRatio.toString()
    """
    hrfmt = "HardnessRatio: {:6.3f}"
    frame = ""

    if ( hasattr( measure.coord, "hardness_ratio") ):
        
        frame = "band_low: {}, band_high: {}".format(measure.coord.coord_sys.frame.low.name,
                                                     measure.coord.coord_sys.frame.high.name)
        if ( hasattr( measure.coord.hardness_ratio, "value") ):
            coordstr = hrfmt.format( measure.coord.hardness_ratio.value )
        else:
            coordstr = hrfmt.format( measure.coord.hardness_ratio )
    else:
        raise(TypeError("Unsupported HardnessRatio type ({})".format(str(type(measure.coord)))))

    errstr = ""
    if measure.error is not None:
        errstr = " " + error_toString( measure.error.stat_error )

    # Add Frame Info
    result = coordstr + errstr + " [{}]".format(frame)

    return result

def flag_toString( measure ):
    """
    proxy for mango:Flag.toString()
    """
    flagfmt = "Flag: {:d} [{}]"

    # find interpretaton of value in CoordSys
    if ( hasattr( measure.coord, "status" ) ):
        grade = [rec.label for rec in measure.coord.coord_sys.status_labels if rec.value == measure.coord.status]
        result = flagfmt.format( measure.coord.status, grade[0] )
    else:
        raise(TypeError("Unsupported Flag type ({})".format(str(type(measure.coord)))))

    return result


def error_toString( error ):
    """
    proxy for meas:Uncertainty.toString()
    """
    symmetrical  = "+/- {:6.3e}"
    asymmetrical = "range(low:{:6.3f}, high:{:6.3f})"
    ellipse      = "ellipse(major:{:6.3e}, minor:{:6.3e}, angle:{:6.3f})"
    
    if ( hasattr( error, "radius" ) ):
        if ( hasattr( error.radius, "value" ) ):
            result = symmetrical.format(error.radius.value)
        else:
            result = symmetrical.format(error.radius)

    elif ( hasattr( error, "lo_limit" ) ):
        if ( hasattr( error.lo_limit, "value" ) ):
            result = asymmetrical.format(error.lo_limit.value, error.hi_limit.value)
        else:
            result = asymmetrical.format(error.lo_limit, error.hi_limit)

    elif ( hasattr( error, "semi_axis" ) ):
        if ( hasattr( error.semi_axis[0], "value" ) ):
            semi_major = error.semi_axis[0].value
            semi_minor = error.semi_axis[1].value
            pos_angle  = float('nan') if error.pos_angle is None else error.pos_angle.value
        else:
            semi_major = error.semi_axis[0]
            semi_minor = error.semi_axis[1]
            pos_angle  = error.pos_angle

        result = ellipse.format( semi_major, semi_minor, pos_angle )
    else:
        raise(TypeError("Unrecognized Error type ({})".format(str(type(error)))))

    return result
    

