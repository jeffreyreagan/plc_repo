from pylogix import PLC
import struct

def convert_timer_bytes_to_readable(timer_bytes):
    try:
        # Assuming a 12-byte timer value representing time in milliseconds
        milliseconds = struct.unpack('Q', timer_bytes[:8])[0]  # Extract the first 8 bytes
        additional_data = struct.unpack('I', timer_bytes[8:])[0]  # Extract the remaining 4 bytes as a 32-bit integer
        
        # Convert milliseconds to a readable format
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        return f"{hours}h {minutes}m {seconds}s {milliseconds}ms Additional Data: {additional_data}"
    except struct.error:
        return "Unsupported timer format"

def read_all_tags(plc_ip):
    with PLC() as plc:
        # Establish connection to the PLC
        plc.IPAddress = plc_ip

        # Get a list of all tags in the PLC
        response = plc.GetTagList()

        # Check if response is not None before accessing response.Value
        if response is not None and response.Value is not None:
            all_tags = response.Value

            # Read and print the name, value, and data type of each tag
            for tag in all_tags:
                try:
                    tag_name = tag.TagName
                    tag_value = plc.Read(tag_name).Value

                    # Convert the timer byte array to a readable format
                    if tag.DataType == 'TIMER':
                        tag_value = convert_timer_bytes_to_readable(tag_value)

                    tag_data_type = tag.DataType
                    print(f"Tag: {tag_name}, Value: {tag_value}, Data Type: {tag_data_type}")
                except Exception as e:
                    print(f"Error reading tag {tag_name}: {e}")
        else:
            print("Failed to get tag list or no tags found. Check PLC connection and configuration.")


if __name__ == "__main__":
    plc_ip_address = "172.16.31.61"
    read_all_tags(plc_ip_address)
