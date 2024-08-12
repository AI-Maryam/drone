import csv
import xml.etree.ElementTree as ET
from datetime import datetime

def csv_to_xml(csv_file, xml_file):
    # Create the root element
    root = ET.Element("Robin")
    
    # Create SystemStatus element
    system_status = ET.SubElement(root, "SystemStatus")
    system_status.set("timestamp", datetime.utcnow().isoformat())
    
    # Create Name element
    name = ET.SubElement(system_status, "Name")
    name.text = "ROBIN_IRIS"
    
    # Create Version element
    version = ET.SubElement(system_status, "Version")
    version.text = "23.07.0 (10729, 70101a5889)"
    
    # Create OperationalState element
    operational_state = ET.SubElement(system_status, "OperationalState")
    operational_state.text = "operational"
    
    # Create Messages element
    messages = ET.SubElement(system_status, "Messages")
    
    # Read the CSV file
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create Sensors element
            sensors = ET.SubElement(system_status, "Sensors")
            
            # Create SensorStatus element
            sensor_status = ET.SubElement(sensors, "SensorStatus")
            sensor_status.set("id", "0")
            
            # Create Name element under SensorStatus
            sensor_name = ET.SubElement(sensor_status, "Name")
            sensor_name.text = "GPS"
            
            # Create Version element under SensorStatus
            sensor_version = ET.SubElement(sensor_status, "Version")
            sensor_version.text = "23.07.0 (10729, 70101a5889)"
            
            # Create OperationalState element under SensorStatus
            sensor_operational_state = ET.SubElement(sensor_status, "OperationalState")
            sensor_operational_state.text = "operational"
            
            # Create Position element under SensorStatus
            position = ET.SubElement(sensor_status, "Position")
            latitude = ET.SubElement(position, "Latitude")
            latitude.text = row["latitude"]
            longitude = ET.SubElement(position, "Longitude")
            longitude.text = row["longitude"]
            altitude = ET.SubElement(position, "Altitude")
            altitude.text = row["altitude (m)"]
            
            # Create GroundLevel element under SensorStatus
            ground_level = ET.SubElement(sensor_status, "GroundLevel")
            ground_level.text = "5.0"
            
            # Create Orientation element under SensorStatus
            orientation = ET.SubElement(sensor_status, "Orientation")
            azimuth = ET.SubElement(orientation, "Azimuth")
            azimuth.text = "135.13998413"
            elevation = ET.SubElement(orientation, "Elevation")
            elevation.text = "0.00000000"
            
            # Create SensorType element under SensorStatus
            sensor_type = ET.SubElement(sensor_status, "SensorType")
            sensor_type.text = "3DSearchRadar"
            
            # Create BlankingSector elements under SensorStatus
            for _ in range(2):
                blanking_sector = ET.SubElement(sensor_status, "BlankingSector")
                angle = ET.SubElement(blanking_sector, "Angle")
                angle.text = "0.00000000"
                span = ET.SubElement(blanking_sector, "Span")
                span.text = "0.00000000"
            
            # Create Processing element under SensorStatus
            processing = ET.SubElement(sensor_status, "Processing")
            operating_mode_id = ET.SubElement(processing, "OperatingModeID")
            operating_mode_id.text = "DYNAMIC"
            ready = ET.SubElement(processing, "Ready")
            ready.text = "true"
            dynamic_positioning = ET.SubElement(processing, "DynamicPositioning")
            dynamic_positioning.text = "true"
            
            # Create Messages element under SensorStatus
            sensor_messages = ET.SubElement(sensor_status, "Messages")
            message = ET.SubElement(sensor_messages, "Message")
            message.set("id", "1")
            message.set("timestamp", datetime.utcnow().isoformat())
            message.set("severity", "info")
            message.text = "Constructing"
            
            # Create Components element under SensorStatus
            components = ET.SubElement(sensor_status, "Components")
            for component_name in ["Transceiver", "Data", "MotorController", "Database", "GPS", "Magnetometer"]:
                component = ET.SubElement(components, component_name)
                component.set("initialized" if component_name == "Transceiver" else "connected", "false")
                component.set("running", "false")
                if component_name == "GPS":
                    component.set("Ready", "false")
                    component.set("Lock", "false")
                    component.set("HDOP", "20.0")
                if component_name == "Magnetometer":
                    component.set("Ready", "false")
                    component.set("Sensitivity", "0.0")

    # Convert the tree to a string
    tree_str = ET.tostring(root, encoding='utf8').decode('utf8')
    
    # Save the string to the XML file
    with open(xml_file, 'w') as f:
        f.write(tree_str)

csv_file = 'updated_drone_data.csv'  # Path to your CSV file
xml_file = 'output.xml'  # Path to save the XML file
csv_to_xml(csv_file, xml_file)
