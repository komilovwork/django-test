import docker
import uuid
import tarfile
import os
from io import BytesIO
from schemas import CodeResponse

client = docker.from_env()

def create_tarfile(files):
    """Create a tar archive of the given files."""
    tar_stream = BytesIO()
    with tarfile.open(fileobj=tar_stream, mode='w') as tar:
        for file_path, arcname in files:
            tar.add(file_path, arcname=arcname)
    tar_stream.seek(0)
    return tar_stream

def execute_python_code(code: str) -> CodeResponse:
    container_name = f"python_executor_{uuid.uuid4().hex[:8]}"  # Unique name

    # Define script filename inside the container
    script_filename = "script.py"

    # Define temp directory to store files before mounting
    temp_dir = "/tmp/docker_code_exec"
    os.makedirs(temp_dir, exist_ok=True)

    script_path = os.path.join(temp_dir, script_filename)

    # Save the user code into a script file
    with open(script_path, "w") as f:
        f.write(code)

    try:
        # Create the container without running it yet
        container = client.containers.create(
            image="python:3.10",
            command=["python3", f"/app/{script_filename}"],
            mem_limit="128m",  # Limit memory usage
            cpu_period=100000,
            cpu_quota=50000,  # Restrict CPU to 50%
            network_disabled=True,  # Prevent networking
            name=container_name
        )

        # Create a tar archive of the Python file
        tar_stream = create_tarfile([(script_path, f"app/{script_filename}")])

        # Copy the script into the container
        client.api.put_archive(container.id, "/", tar_stream)

        # Start the container
        container.start()

        # Wait for execution and capture logs
        wait_result = container.wait()
        exit_code = wait_result["StatusCode"] if isinstance(wait_result, dict) else wait_result
        output = container.logs().decode("utf-8")

        # Remove the container after execution
        container.remove()

        return CodeResponse(output=output if exit_code == 0 else "", error=output if exit_code != 0 else "")

    except docker.errors.ContainerError as e:
        return CodeResponse(output="", error=str(e))

    except docker.errors.APIError as e:
        return CodeResponse(output="", error="Docker API error: " + str(e))

    except Exception as e:
        return CodeResponse(output="", error="Unexpected error: " + str(e))
