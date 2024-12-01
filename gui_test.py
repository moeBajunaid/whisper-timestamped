from gooey import Gooey, GooeyParser
import subprocess
import os

@Gooey(program_name="Scribe-Mercury", tabbed_groups=True)
def main():
    parser = GooeyParser(description="Logbook Digitization Tool")
    
    # First tab
    recording_group = parser.add_argument_group('Audio File Transcription', description='Settings for Speech-to-Text transcription')
    recording_group.add_argument('COMM_File', help='Input comm file for transcription', widget='FileChooser', gooey_options={'full_width': True})
    recording_group.add_argument('STT_Model', choices=['Whisper_v3_turbo', 'Whisper_v3_small', 'Other'], help='Select your STT model', gooey_options={'full_width': True})
    

    # Second tab
    live_group = parser.add_argument_group('Live Voice Configuration', description='For future implementation')
    live_group.add_argument('--STT_Model_Copy', choices=['Whisper_v3_turbo', 'Whisper_v3_small', 'Other'], help='Select your STT model', gooey_options={'full_width': True, 'disabled': True})
    live_group.add_argument('--verbose', action='store_true', help='Enable verbose output')
    live_group.add_argument('-ss', metavar='Timestamp', help='Timestamp of snapshot (in seconds)')
    live_group.add_argument('-frames:v', metavar='Timestamp', default=1, gooey_options={'visible': False})

    args = parser.parse_args()
    audio_path = args.COMM_File
    # Ensure the STT_Model_Copy is the same as STT_Model
    if args.STT_Model_Copy is None:
        args.STT_Model_Copy = args.STT_Model


    try:
        # Call whisper_test.py and capture its output
        
        command = ["python3","test_whisper.py",audio_path]
       
        result = subprocess.Popen(command, 
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT)
        
        print("location of selected audio file: " + audio_path)
        resultingOutput = []
        for line in result.stdout:
            resultingOutput.append(line.decode('utf-8'))
        
        allText = "\n".join(resultingOutput)
        squareBracketIndex = allText.rindex(']')
        print(allText[squareBracketIndex+1:])
        result.wait()
       
    except subprocess.TimeoutExpired:
        print("Error: whisper_test.py timed out.")
    except subprocess.CalledProcessError as e:
        print(f"Error: whisper_test.py failed with error code {e.returncode}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    if args.verbose:
        print("Verbose mode enabled")



def display_results(output):
    @Gooey(program_name="Subprossess Results")
    def show_results():
        parser = GooeyParser(description="Results of the subprocess")
        parser.add_argument("Output", widget="Textarea", default=output, help="Transcript English text")
        parser.parse_args()
    show_results()

if __name__ == '__main__':
    main()

