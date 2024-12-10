from flask import jsonify, session
from model import db, Notification
from notification import notification_bp
from utils.auth_helpers import login_required

@login_required
@notification_bp.route('/get-notifications', methods=['GET'])
def get_notifications():
    user_id = session['user_id']
    
    if not user_id:
        return jsonify({"message": "User ID is missing"}), 400

    notifications = Notification.query.filter_by(user_id=user_id).all()
    
    if not notifications:
        return jsonify({"notifications": []})

    notifications_data = [notification.to_dict() for notification in notifications]
    return jsonify({"notifications": notifications_data})

@login_required
@notification_bp.route('/delete-notification/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    notification = Notification.query.get(notification_id)

    if not notification:
        return jsonify({"message": "Notification not found"}), 404

    try:
        db.session.delete(notification)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting notification: {str(e)}"}), 500

    return jsonify({"message": "Notification deleted successfully"})
