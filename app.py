from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # Get JSON data from the request
    data = request.get_json()

    # Check that a title was provided
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Create a new Event
    new_event = Event(len(events) + 1, data["title"])

    # Add the new event to our in-memory database
    events.append(new_event)

    # Return the new event as JSON
    return jsonify(new_event.to_dict()), 201


# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Get JSON data from the request
    data = request.get_json()

    # Check that a title was provided
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Look for the event with the requested ID
    for event in events:
        if event.id == event_id:
            # Update the event title
            event.title = data["title"]

            # Return the updated event
            return jsonify(event.to_dict()), 200

    # If no event was found
    return jsonify({"error": "Event not found"}), 404


# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Look for the event with the requested ID
    for event in events:
        if event.id == event_id:
            # Remove the event from the list
            events.remove(event)

            # Return 204 because the deletion was successful
            return "", 204

    # If no event was found
    return jsonify({"error": "Event not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)