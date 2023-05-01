import subprocess

# Define the command to execute the Bash script with arguments
command = ['bash', 'smssudo_runfile', 'smsmemory_info']

# Execute the command and capture the output and error streams
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Decode the output and error streams from bytes to strings
output = result.stdout.decode('utf-8')
error = result.stderr.decode('utf-8')

# Get the exit code of the process
exit_code = result.returncode

# Check if the command was successful or not
if exit_code == 0:
    print("Command was successful")
else:
    pass
    #print(f"Command failed with exit code {exit_code}")

# Print the output and error streams
print("Output:")
print(output)
print("Error:")
print(error)
