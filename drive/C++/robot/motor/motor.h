

class Motor{
  static int count;
  static double homeAngle;

  public:
    Motor();

    double getAngle();

    void setAngle(double);

    void center();

    void setVelocity(double);

    double getVelocity();

};
