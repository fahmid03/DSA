import java.util.*;


interface SmartDevice{
    void activate();
    void deactivate();
    double getPowerUsage();
    String getStatus();
}

interface ManyDevice extends SmartDevice{
    String getName();
    List <SmartDevice> getDevices();
    void addDevice();
}

class SmartLight implements SmartDevice{
    private boolean enlightened=false;
    public void activate(){
        enlightened=true;
    }
    public void deactivate(){
        enlightened=false;
    }
    public double getPowerUsage(){
        return enlightened?10:0;
    }
    public String getStatus(){
        return "light"+(enlightened?"on":"off");
    }
}

class SmartThermostat implements SmartDevice{
    private boolean heated=false;
    public void activate(){
        heated=true;
    }
    public void deactivate(){
        heated=false;
    }
    public double getPowerUsage(){
        return heated?150:0;
    }
    public String getStatus(){
        return "thermostat"+(heated?"on":"off");
    }
}

class SmartSpeaker implements SmartDevice{
    private boolean singing=false;
    public void activate(){
        singing=true;
    }
    public void deactivate(){
        singing=false;
    }
    public double getPowerUsage(){
        return singing?5:0;
    }
    public String getStatus(){
        return "speaker"+(singing?"playing":"idle");
    }
}

class Room implements SmartDevice{
    private final String name;
    private final List<SmartDevice> devices=new ArrayList<>();
    public Room(String name){
        this.name=name;
    }
    public void activate(){
        for (SmartDevice device:devices){
            device.activate();
        }
    }
    public void deactivate(){
        for (SmartDevice device:devices){
            device.deactivate();
        }
    }
    public double getPowerUsage(){
        double total=0;
        for (SmartDevice device:devices){
            total+=device.getPowerUsage();
        }
        return total;
    }
    public String getStatus(){
        StringBuilder bigstring=new StringBuilder(name);
        for (SmartDevice device:devices){
            bigstring.append("\n").append(device.getStatus());
        }
        return bigstring.toString();
    }
    public void addDevice(SmartDevice device){
        devices.add(device);
    }
    public List<SmartDevice> getDevices(){
        return devices;
    }
}

class Home implements SmartDevice{
    private final String name;
    private final List<SmartDevice> rooms=new ArrayList<>();
    public Home(String name){
        this.name=name;
    }
    public void activate(){
        for (SmartDevice room:rooms){
            room.activate();
        }
    }
    public void deactivate(){
        for (SmartDevice room:rooms){
            room.deactivate();
        }
    }
    public double getPowerUsage(){
        double total=0;
        for (SmartDevice room:rooms){
            total+=room.getPowerUsage();
        }
        return total;
    }
    public String getStatus(){
        StringBuilder biggerstring=new StringBuilder("home sweer"+name+" home");
        for (SmartDevice device:rooms){
            biggerstring.append("\n").append(device.getStatus());
        }
        return biggerstring.toString();
    }
    public void addRoom(SmartDevice room){
        rooms.add(room);
    }
    public List<SmartDevice> getRooms(){
        return rooms;
    }
}

abstract class DeviceDecorator implements SmartDevice{
    protected final SmartDevice cleanslate;
    public DeviceDecorator(SmartDevice device){
        this.cleanslate=device;
    }
    public SmartDevice getDecorated(){
        return cleanslate;
    }
    public void activate(){
        cleanslate.activate();
    }
    public void deactivate(){
        cleanslate.deactivate();
    }
    public double getPowerUsage(){
        return cleanslate.getPowerUsage();
    }
    public String getStatus(){
        return cleanslate.getStatus();
    }
}

class AccessRestricted extends DeviceDecorator{
    private final int pinnum;
    private boolean locked=true;
    public AccessRestricted(SmartDevice device,int pin){
        super(device);
        this.pinnum=pin;
    }
    public void unlock(int triedpin){
        if(this.pinnum==triedpin){
            this.locked=false;
        }
    }
    public void lock(){
        this.locked=true;
    }
    public void activate(){
        if(!locked){
            super.activate();
        }
    }
    public void deactivate(){
        if(!locked){
            super.deactivate();
        }
    }
    public String getStatus() {
        String superstring = super.getStatus();
        if (locked) {
            return superstring + " LOCKED";
        }
        return superstring;
    }
}

class TimerControlled extends DeviceDecorator{
    private final int duration;
    private boolean isTimed=true;
    public TimerControlled(SmartDevice device,int time){
        super(device);
        this.duration=time;
    }
    public void activate(){
        super.activate();
        isTimed=true;
    }
    public void deactivate(){
        super.deactivate();
        this.isTimed=false;
    }
    public String getStatus() {
        String superstring = super.getStatus();

        if (isTimed) {
            return superstring + " auto-off in " + duration + "s";
        }

        return superstring + " (timer is off)";
    }
    public void simulateTimerExpiry(){
        if(isTimed){
            super.deactivate();
            this.isTimed=false;
        }
    }
}

class PowerThrottled extends DeviceDecorator{
    private final double powerlimit;
        public PowerThrottled(SmartDevice device,double limit){
        super(device);
        this.powerlimit=limit;
    }
    public String getStatus(){
        String superstring=super.getStatus();
        double consumption=getPowerUsage();
        if(consumption>0&&super.getPowerUsage()>powerlimit){
            return superstring + " throttled to " + powerlimit + "W";
        }
        return superstring;
    }
    public double getPowerUsage(){
        double power=super.getPowerUsage();
        return Math.min(power,powerlimit);
    }
}

class EcoMode extends DeviceDecorator{
    private final Room room;
    private final double budget;
    public EcoMode(Room room, double budget){
        super(room);
        this.room=room;
        this.budget=budget;
    }
    public void activate() {
        super.activate();
        enforceBudget();
    }
    private void enforceBudget(){
        List<SmartDevice> devices=room.getDevices();
        for(int i=devices.size()-1;i>=0;i--){
            if(getPowerUsage()<=budget){
                break;
            }
            devices.get(i).deactivate();
        }
    }
    public String getStatus(){
        String superstring=super.getStatus();
        return "ECO "+budget+"W budget\n"+superstring;
    }
}
class GuestMode extends DeviceDecorator{
    private final Room room;
    private final Set<Class<?>> allowed;
    public GuestMode(Room room,Set<Class<?>> allowed){
        super(room);
        this.room=room;
        this.allowed=allowed;
    }
    private SmartDevice unwrap(SmartDevice device){
        while(device instanceof DeviceDecorator){
            device=((DeviceDecorator)device).getDecorated();
        }
        return device;
    }
    private boolean isAllowed(SmartDevice device){
        SmartDevice base=unwrap(device);;
        for(Class<?> allowedclass:allowed){
            if (allowedclass.isInstance(base)){
                return true;
            }
        }
        return false;
    }
    public void activate(){
        for(SmartDevice device:room.getDevices()){
            if(isAllowed(device)){
                device.activate();
            }
        }
    }
    public void deactivate(){
        for(SmartDevice device:room.getDevices()){
            if(isAllowed(device)){
                device.deactivate();
            }
        }
    }
    public double getPowerUsage(){
        double total=0;
        for(SmartDevice device:room.getDevices()){
            if(isAllowed(device)){
                total+=device.getPowerUsage();
            }
        }
        return total;
    }

    public String getStatus(){
        StringBuilder bigstring=new StringBuilder("Guest mode\n"+getRoom());
        for(SmartDevice device:room.getDevices()){
            bigstring.append("\n").append(device.getStatus());
            if(!isAllowed(device)){
                bigstring.append("guest-restricted");
            }
        }
        return bigstring.toString();
    }

    private String getRoom(){
        String status=room.getStatus();
        int start=status.indexOf("[");
        int end=status.indexOf("]");
        if(start!=-1&&end!=-1){
            return status.substring(start+1,end);
        }
        return "Room";
    }
}

public class SmartHome {

    public static void main(String[] args) {
        demoA();
        demoB();
        demoC();
        demoD();
        demoE();
        demoF();
    }

    static void header(String title) {
        System.out.println("\n" + "=".repeat(55));
        System.out.println("  " + title);
        System.out.println("=".repeat(55));
    }

    static void demoA() {
        header("DEMO A: Home Overview");

        Room living = new Room("Living Room");
        living.addDevice(new SmartLight());
        living.addDevice(new SmartSpeaker());

        Room bedroom = new Room("Bedroom");
        bedroom.addDevice(new SmartLight());
        bedroom.addDevice(new SmartThermostat());

        Home home = new Home("My Home");
        home.addRoom(living);
        home.addRoom(bedroom);

        System.out.println("Before activation:");
        System.out.println(home.getStatus());
        System.out.println("Power: " + home.getPowerUsage() + "W");

        home.activate();
        System.out.println("\nAfter activation:");
        System.out.println(home.getStatus());
        System.out.println("Power: " + home.getPowerUsage() + "W");
    }

    static void demoB() {
        header("DEMO B: AccessRestricted + TimerControlled");

        SmartLight baseLight = new SmartLight();
        AccessRestricted restrictedLight = new AccessRestricted(baseLight, 1234);
        TimerControlled light = new TimerControlled(restrictedLight, 60);

        System.out.println("Step 1 - Try to activate while locked:");
        light.activate();
        System.out.println("Status: " + light.getStatus());
        System.out.println("Power: " + light.getPowerUsage() + "W");

        System.out.println("\nStep 2 - Wrong PIN:");
        restrictedLight.unlock(0000);
        System.out.println("Attempted to unlock with incorrect PIN.");
        light.activate();
        System.out.println("Status: " + light.getStatus());
        System.out.println("Power: " + light.getPowerUsage() + "W");

        System.out.println("\nStep 3 - Correct PIN:");
        restrictedLight.unlock(1234);
        System.out.println("Unlocked with correct PIN.");
        light.activate();
        System.out.println("Status: " + light.getStatus());
        System.out.println("Power: " + light.getPowerUsage() + "W");

        System.out.println("\nStep 4 - Timer expires:");
        light.simulateTimerExpiry();
        System.out.println("Status: " + light.getStatus());
        System.out.println("Power: " + light.getPowerUsage() + "W");
    }


    static void demoC() {
        header("DEMO C: EcoMode (budget = 100W)");

        Room office = new Room("Office");
        office.addDevice(new SmartLight());
        office.addDevice(new SmartLight());
        office.addDevice(new SmartThermostat());
        SmartDevice ecoOffice = new EcoMode(office, 100);

        ecoOffice.activate();


        System.out.println("Activating with EcoMode:");
        ecoOffice.activate();
        System.out.println(ecoOffice.getStatus());
        System.out.println("Power: " + ecoOffice.getPowerUsage() + "W");
    }


    static void demoD() {
        header("DEMO D: Order Matters");


        Room room1 = new Room("Lab-1");
        room1.addDevice(new SmartLight());
        room1.addDevice(new SmartLight());
        SmartDevice thermo =
        new PowerThrottled(
            new SmartThermostat(),
            80
        );

        room1.addDevice(thermo);
        SmartDevice ecoRoom = new EcoMode(room1,100);

        System.out.println("Setup 1: Throttled thermostat (80W) + EcoMode(100W)");
        ecoRoom.activate();
        System.out.println(ecoRoom.getStatus());
        System.out.println("Power: " + ecoRoom.getPowerUsage() + "W");

        Room room2 = new Room("Lab-2");
        room2.addDevice(new SmartLight());
        room2.addDevice(new SmartLight());
        room2.addDevice(new SmartThermostat());
        SmartDevice ecoRoom2 = new EcoMode(room2,100);

        System.out.println("\nSetup 2: Raw thermostat (150W) + EcoMode(100W)");
        ecoRoom2.activate();
        System.out.println(ecoRoom2.getStatus());
        System.out.println("Power: " + ecoRoom2.getPowerUsage() + "W");
    }


    static void demoE() {
        header("DEMO E: GuestMode + Mixed Enhancements");

        Room guest = new Room("Guest Room");

        guest.addDevice(new SmartSpeaker());

        guest.addDevice(
            new AccessRestricted(
                new SmartThermostat(),
                9999
            )
        );

        guest.addDevice(
            new TimerControlled(
                new SmartLight(),
                120
            )
        );

        Set<Class<?>> allowed = new HashSet<>();
        allowed.add(SmartLight.class);
        allowed.add(SmartSpeaker.class);

        SmartDevice guestRoom = new GuestMode(guest, allowed);

        System.out.println("Activating GuestMode room:");
        guestRoom.activate();
        System.out.println("\n" + guestRoom.getStatus());
        System.out.println("Guest-visible power: " + guestRoom.getPowerUsage() + "W");
    }

    static void demoF() {
        header("DEMO F: prepareForNight wraps a Room");

        Room kids = new Room("Kids Room");
        kids.addDevice(new SmartLight());
        kids.addDevice(new SmartSpeaker());
        kids.addDevice(new SmartThermostat());


        boolean roomLocked = true;
        int roomPin = 0;
        int roomTimerSeconds = 3600;
        boolean roomTimerRunning = false;

        System.out.println("Step 1 — Activate while locked (nothing happens):");
        if (!roomLocked) {
            kids.activate();
        }

        
        System.out.println("  Status:\n" + kids.getStatus() + " [LOCKED]");
        System.out.println("  Power: " + kids.getPowerUsage() + "W");

        System.out.println("\nStep 2 — Unlock and activate:");
        if (0 == roomPin) { roomLocked = false; System.out.println("    >> Unlock SUCCESS"); }
        if (!roomLocked) {
            kids.activate();
            roomTimerRunning = true;
        }
        String timerSuffix = roomTimerRunning ? " (auto-off in " + roomTimerSeconds + "s)" : "";
        System.out.println("  Status:\n" + kids.getStatus() + timerSuffix);
        System.out.println("  Power: " + kids.getPowerUsage() + "W");

        System.out.println("\nStep 3 — Timer expires (entire room shuts off):");
        if (roomTimerRunning) {
            System.out.println("    >> Timer expired — auto-deactivating.");
            kids.deactivate();
            roomTimerRunning = false;
        }
        System.out.println("  Status:\n" + kids.getStatus());
        System.out.println("  Power: " + kids.getPowerUsage() + "W");

        System.out.println("\nStep 4 — Add to Home:");
        Home home = new Home("Night Home");
        home.addRoom(kids); 
        System.out.println("  Home power: " + home.getPowerUsage() + "W");

    }
}