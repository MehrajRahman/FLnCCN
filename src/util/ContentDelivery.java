package util;

public class ContentDelivery {
    private String contentKey;
    private double deliveryTime;

    public ContentDelivery(String key, double time) {
        this.contentKey = key;
        this.deliveryTime = time;
    }

    public String getContentKey() { return contentKey; }
    public double getDeliveryTime() { return deliveryTime; }
}