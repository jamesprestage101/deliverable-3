import os

# Directory paths
dir_path = 'meets'
image_dir = 'images/athletes'

# Updated HTML header with a top navbar and modal logic fixes
html_header = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="icon" href="images/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" type="text/css" href="css/reset.css">
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <!-- Top Navbar -->
    <div class="navbar">
        <a href="index.html">Home</a>
        <a href="results.html">All Events</a>
        <a href="mens_results.html">Men's Events</a>
        <a href="womens_results.html">Women's Events</a>
    </div>

    <!-- Image Modal -->
    <div id="image-modal" class="modal" style="display: none;">
        <img class="modal-content" id="modal-img" alt="Profile Pic Fullscreen View">
        <div id="modal-caption"></div>
    </div>
"""

# HTML footer content (Back to Top button)
html_footer = """
    <!-- Back to Top Button -->
    <button id="back-to-top" tabindex="0" style="display:none;">Back to Top</button>
</body>
</html>
"""

# Function to create HTML for event sections
def create_event_sections(gender=None):
    sections = ""
    event_count = 0
    medals = ["&#129351;", "&#129352;", "&#129353;"]

    for filename in os.listdir(dir_path):
        if filename.endswith('.csv'):
            event_name = os.path.splitext(filename)[0].replace('_', ' ')
            if (gender == "Men" and "Men" not in event_name) or (gender == "Women" and "Women" not in event_name):
                continue

            event_count += 1
            file_path = os.path.join(dir_path, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()

            team_scores, individual_results = [], []
            in_team_scores, in_individual_results = False, False

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
                elif not line:
                    continue

                if in_team_scores and len(team_scores) < 3:
                    team_scores.append(line.split(','))
                elif in_individual_results and len(individual_results) < 3:
                    individual_results.append(line.split(','))

            sections += f"""
            <div class="spacer" id="spacer-{event_count}"></div>
            <section id="event-{event_count}" class="event">
                <h2>{event_name}</h2>
                <h3>Team Scores</h3>
                <div class="podium">
            """
            for idx, score in enumerate(team_scores):
                medal_icon = medals[idx] if idx < 3 else ""
                position_class = "first-place" if idx == 0 else "second-place" if idx == 1 else "third-place"
                sections += f"""
                <div class="{position_class}">
                    <p><b>{medal_icon} {score[1]}</b></p>
                    <p>Score: {score[2]}</p>
                </div>
                """
            sections += """
                </div>
                <br>
                <h3>Top 3 Results</h3>
                <table class="athlete-table">
                    <thead>
                        <tr>
                            <th>Place</th>
                            <th>Grade</th>
                            <th>Name</th>
                            <th>Time</th>
                            <th>Team</th>
                            <th>Profile</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for result in individual_results:
                if len(result) >= 7:
                    athlete_link = result[3]
                    athlete_id = athlete_link.split('/')[-2]
                    image_path = os.path.join(image_dir, f"{athlete_id}.jpg")
                    image_src = f"images/athletes/{athlete_id}.jpg" if os.path.exists(image_path) else "images/default.jpg"
                    sections += f"""
                    <tr>
                        <td data-label="Place">{result[0]}</td>
                        <td data-label="Grade">{result[1]}</td>
                        <td data-label="Name"><a href="{athlete_link}" target="_blank">{result[2]}</a></td>
                        <td data-label="Time">{result[4]}</td>
                        <td data-label="Team">{result[5]}</td>
                        <td data-label="Profile">
                            <img src="{image_src}" alt="Profile Picture of {result[2]}" 
                                 onclick="toggleModal('{image_src}', '{result[2]}', event)" 
                                 tabindex="0">
                        </td>
                    </tr>
                    """
            sections += """
                    </tbody>
                </table>
            </section>
            """
    return sections

# Generate HTML pages
pages = [("results.html", "All 2024 Event Summaries", None),
         ("mens_results.html", "&#9794; Men's Event Summaries", "Men"),
         ("womens_results.html", "&#9792; Women's Event Summaries", "Women")]

for filename, title, gender_filter in pages:
    html_content = html_header.format(title=title)
    html_content += """
    <main>
        <nav class="event-list">
            <ul>
    """

    # Event list based on gender filter
    event_count = 0
    for event_filename in os.listdir(dir_path):
        if event_filename.endswith('.csv'):
            event_name = os.path.splitext(event_filename)[0].replace('_', ' ')
            if (gender_filter == "Men" and "Men" not in event_name) or (gender_filter == "Women" and "Women" not in event_name):
                continue
            event_count += 1
            html_content += f'<li><a href="#event-{event_count}" class="event-link">{event_name}</a></li>'

    html_content += f"""
            </ul>
        </nav>
        <h1>{title}</h1>
    """

    html_content += create_event_sections(gender=gender_filter)
    html_content += """
    <script src="js/script.js"></script>
    </main>
    """
    html_content += html_footer

    # Save each page to a file
    with open(filename, 'w') as file:
        file.write(html_content)

    print(f'{filename} generated successfully.')