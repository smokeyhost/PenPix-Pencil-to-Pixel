import NotificationSwitch from "./NotificationSwitch";

const NotificationSetting = () => {
  return (
    <div className="flex flex-col gap-2">
      <h2 className="text-lg font-semibold">Notifications</h2>
      <div className="ml-4 flex flex-col gap-2">
        <NotificationSwitch text="New Submission"/>
        <NotificationSwitch text="Completed Submissions"/>
        <NotificationSwitch text="Due Date"/>
      </div>
    </div>
  );
};

export default NotificationSetting;
