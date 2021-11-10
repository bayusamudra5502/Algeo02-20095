export default function Progress({ value, animated }) {
  return (
    <div className="progress">
      <div
        className={
          "progress-bar progress-bar-striped bg-proses-ok " +
          (animated ? "progress-bar-animated" : "")
        }
        style={{ width: `${value * 100}%`, height: "100%" }}
      ></div>
    </div>
  );
}
