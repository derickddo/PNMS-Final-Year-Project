def population_projection_prompt (population_projection_contex):
    return f'Generate a comprehensive report based on the provided population projection data. The report should be clean, well-organized, and visually appealing, following a consistent style. {population_projection_contex}. Here are the structure of the report: 1. Introduction 2. Population Projection Data 3. Population Projection Analysis 4. Conclusion. Do not include tables'




def needs_assessment_prompt (needs_assessment_context):
    return f'Create a needs assessment report based on the provided data. The report should be well-organized, visually appealing, and easy to read. Include tables to present data clearly and modify them to look professional and engaging. {needs_assessment_context}. The report should include the following sections: 1. Introduction 2. Facility Needs 3. Personnel Needs 4. Classroom Needs 5. Dual Desk Needs 6. Water Needs 7. Skip Container Needs 8. Conclusion. Do not include tables'

def map_prediction_prompt (map_prediction_context):
    return f'Create a map prediction report based on the provided data. The report should be visually appealing, easy to understand, and well-organized. Include maps, charts, and tables to present data clearly and modify them to look professional and engaging. {map_prediction_context}. Insert tables where necessary to present detailed data. The tables should be well-formatted, with appropriate headings, borders, and alternate row shading for better readability. make the tables in html format and tailwind css classes for styling. '

