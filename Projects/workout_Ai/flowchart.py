from graphviz import Digraph

# Initialize the graph
flowchart = Digraph(comment='Dumbbell Curl Rep Counter Flowchart')
flowchart.attr(size='10,10')

# Define nodes for flowchart steps
flowchart.node('A', 'Start')
flowchart.node('B', 'Initialize MediaPipe Pose Model')
flowchart.node('C', 'Initialize Video Capture')
flowchart.node('D', 'Initialize Text-to-Speech Engine')
flowchart.node('E', 'While True')
flowchart.node('F', 'Capture Frame from Camera')
flowchart.node('G', 'Flip Frame for Selfie View')
flowchart.node('H', 'Convert Frame to RGB')
flowchart.node('I', 'Process Frame for Pose Detection')
flowchart.node('J', 'Pose Landmarks Detected?')
flowchart.node('K', 'Calculate Elbow Angles')
flowchart.node('L', 'Draw Progress Bar')
flowchart.node('M', 'Display Overlay with Info')
flowchart.node('N', 'Check Arm Position')
flowchart.node('O', 'Stage = "Down"?')
flowchart.node('P', 'Rep Count += 1\nVoice Feedback')
flowchart.node('Q', 'Draw Pose Landmarks on Frame')
flowchart.node('R', 'Display Frame')
flowchart.node('S', 'Exit on "q" Key Press')
flowchart.node('T', 'Release Resources and End')

# Define edges for flowchart
flowchart.edges(['AB', 'BC', 'CD', 'DE', 'EF', 'FG', 'GH', 'HI', 'IJ'])  # Initialization and loop start
flowchart.edge('J', 'K', label='Yes')
flowchart.edge('J', 'F', label='No')  # If no pose detected, return to capture frame
flowchart.edge('K', 'L')
flowchart.edge('L', 'M')
flowchart.edge('M', 'N')
flowchart.edge('N', 'O', label='If Arms Fully Extended')
flowchart.edge('O', 'P', label='If Flexed (Curl Up)')
flowchart.edge('P', 'R', label='Rep Completed')
flowchart.edge('O', 'R', label='Else')  # No rep count if only extended
flowchart.edge('R', 'S')
flowchart.edge('S', 'F', label='If "q" Not Pressed')
flowchart.edge('S', 'T', label='If "q" Pressed')

# Render the flowchart
flowchart.render('/mnt/data/dumbbell_curl_rep_counter_flowchart', format='png', view=False)
'/mnt/data/dumbbell_curl_rep_counter_flowchart.png'
