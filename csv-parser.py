import os

# Path to the directory containing CSV files and images
dir_path = 'deliverable-3/meets'
image_dir = 'deliverable-3/images'

# HTML content to be constructed directly
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Results</title>
    <link rel="stylesheet" type="text/css" href="css/reset.css"> 
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <h1>Results</h1>
"""

# Loop through each file in the directory
for filename in os.listdir(dir_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(dir_path, filename)
        
        # Extract event name from the filename (assuming the filename has meaningful event info)
        event_name = os.path.splitext(filename)[0].replace('_', ' ')

        # Reading the file manually as it contains inconsistent formatting
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Variables to store team scores and individual results
        team_scores = []
        individual_results = []

        # Flags to detect sections
        in_team_scores = False
        in_individual_results = False

        # Loop through lines to capture the relevant data
        for line in lines:
            line = line.strip()

            if line.startswith("Place,Team,Score"):
                in_team_scores = True
                in_individual_results = False
                continue
            elif line.startswith("Place,Grade,Name,Athlete Link,Time,Team,Team Link,Profile Pic"):
                in_team_scores = False
                in_individual_results = True
                continue
            elif not line:  # Ignore empty lines
                continue

            if in_team_scores and len(team_scores) < 3:
                team_scores.append(line.split(','))
            elif in_individual_results and len(individual_results) < 3:
                individual_results.append(line.split(','))

        # Add a new section for each event
        html_content += f"""
        <div class="event">
            <h2>{event_name}</h2>
            <h3>Team Scores</h3>
            <table>
                <thead>
                    <tr>
                        <th>Place</th>
                        <th>Team</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
        """

        # Add team scores to the HTML content
        for score in team_scores:
            if len(score) >= 3:
                html_content += f"""
                    <tr>
                        <td>{score[0]}</td>
                        <td>{score[1]}</td>
                        <td>{score[2]}</td>
                    </tr>
                """

        # Closing the team scores table tag
        html_content += """
                </tbody>
            </table>
            <h3>Top 3 Results</h3>
        """

        # Create the HTML content for athletes
        for result in individual_results:
            if len(result) >= 7:  # Ensure all required data is present
                athlete_link = result[3]
                
                # Extract athlete ID from the link (e.g., https://www.athletic.net/athlete/19229177/cross-country)
                athlete_id = athlete_link.split('/')[-2]
                
                # Define the path to the image using the athlete ID
                image_path = os.path.join(image_dir, f"{athlete_id}.jpg")
                
                # Check if the image exists in the images folder; if not, use a default image
                if os.path.exists(image_path):
                    image_src = f"images/{athlete_id}.jpg"
                else:
                    image_src = f"images/default.jpg"  # Fallback image if athlete's photo isn't available
                
                # Add athlete result to the HTML
                html_content += f"""
                <div class="athlete">
                    <h4>{result[2]}</h4>
                    <p>Place: {result[0]}</p>
                    <p>Grade: {result[1]}</p>
                    <p>Time: {result[4]}</p>
                    <p>Team: {result[5]}</p>
                    <img src="{image_src}" alt="Profile Picture of {result[2]}" width="150">
                </div>
                <hr>
                """

        # Ending the event div
        html_content += """
        </div>
        """

# Closing the HTML tags
html_content += """
</body>
</html>
"""

# Save the HTML content to a file
html_file_path = 'deliverable-3/results.html'
with open(html_file_path, 'w') as file:
    file.write(html_content)

print(f'HTML file generated: {html_file_path}')