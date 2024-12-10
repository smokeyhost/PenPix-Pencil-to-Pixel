import { FaRegBell } from "react-icons/fa";
import { Link, useNavigate } from "react-router-dom";

const Notifications = ({ onClose, notificationsList }) => {
  const navigate = useNavigate();

  const sortedNotifications = [...notificationsList].sort((a, b) => {
    return new Date(b.created_at) - new Date(a.created_at); // Latest first
  });

  return (
    <div className="w-[280px] text-white bg-black text-sm pb-3 pt-2 max-md:w-[250px]">
      <div className="text-white flex items-center gap-2 ml-4">
        <FaRegBell color="white" />
        <span className="font-semibold">Notifications</span>
      </div>
      <div className="w-full max-h-[250px] flex flex-col font-light text-xs mt-4 overflow-y-auto">
        {sortedNotifications.length > 0 ? (
          sortedNotifications.map((notification) => (
            <Link
              to={`/task/${notification.task_id}`}
              key={notification.id}
              className="border-b-1 border-customGray1 py-3 px-5"
              onClick={() => onClose()}
            >
              {notification.message}
            </Link>
          ))
        ) : (
          <div className="text-center text-gray-400">No notifications</div>
        )}
      </div>
      <p
        className="underline italic mt-5 mr-5 text-xs text-right font-normal"
        onClick={() => {
          onClose();
          navigate('/notifications');
        }}
      >
        View all notifications
      </p>
    </div>
  );
};

export default Notifications;
