/**
@implementation of Least Recent Used cache / Utility-Based Federated Cache
*/

package applications; 
import java.util.HashMap;
import core.SimClock;
 
public class LRUCache {
	private HashMap<Integer, DoubleLinkedListNode> map 
		= new HashMap<Integer, DoubleLinkedListNode>();
	private DoubleLinkedListNode head;
	private DoubleLinkedListNode end;
	private int capacity;
	private int len;
	private CCN_application app = null;
 
	public LRUCache(int capacity) {
		this.capacity = capacity;
		len = 0;
	}

	public LRUCache(int capacity, CCN_application app) {
		this.capacity = capacity;
		this.app = app;
		len = 0;
	}
	
	public LRUCache(LRUCache another){
		this.map = another.map;
		this.head = another.head;
		this.end = another.end;
		this.capacity = another.capacity;
		this.len = another.len;
		this.app = another.app;
	}
 
	public String get(int key) {
		if (map.containsKey(key)) {
			DoubleLinkedListNode latest = map.get(key);
			latest.accessCount++;
			latest.lastAccessTime = SimClock.getTime();
			removeNode(latest);
			setHead(latest);
			return latest.val;
		} else {
			return "";
		}
	}
	
	public void print_cache(){
		for(int key:map.keySet()){
			System.out.println("[" + map.get(key).key + "] = " + map.get(key).val);
		}
	}
 
	public void removeNode(DoubleLinkedListNode node) {
		DoubleLinkedListNode cur = node;
		DoubleLinkedListNode pre = cur.pre;
		DoubleLinkedListNode post = cur.next;
 
		if (pre != null) {
			pre.next = post;
		} else {
			head = post;
		}
 
		if (post != null) {
			post.pre = pre;
		} else {
			end = pre;
		}
	}
 
	public void setHead(DoubleLinkedListNode node) {
		node.next = head;
		node.pre = null;
		if (head != null) {
			head.pre = node;
		}
 
		head = node;
		if (end == null) {
			end = node;
		}
	}
 
	private double calculateUtility(DoubleLinkedListNode node) {
		if (app == null) {
			return 0.0;
		}
		
		// 1. Request Probability P_request
		double pRequest = app.getOnlineRequestProbability(node.key);
		
		// 2. Delivery Probability P_deliver
		double pDeliver = app.getOnlineDeliveryProbability();
		
		// 3. Freshness F(u_i)
		int nodeRound = node.key / 1000;
		int currentRound = app.getEstimatedCurrentRound();
		double freshness = 1.0 / (1.0 + Math.max(0, currentRound - nodeRound));
		
		// 4. Aggregation Need A(u_i)
		double aggNeed = (nodeRound >= currentRound) ? 1.0 : 0.0;
		
		// Utility = P_request * P_deliver * F * A
		return pRequest * pDeliver * freshness * aggNeed;
	}

	public void set(int key, String value) {
		System.out.println("LRUCache set: key=" + key + " (Round " + (key/1000) + ") capacity=" + capacity + " len=" + len);
		if (map.containsKey(key)) {
			DoubleLinkedListNode oldNode = map.get(key);
			oldNode.val = value;
			oldNode.accessCount++;
			oldNode.lastAccessTime = SimClock.getTime();
			removeNode(oldNode);
			setHead(oldNode);
		} else {
			DoubleLinkedListNode newNode = 
				new DoubleLinkedListNode(key, value);
			newNode.lastAccessTime = SimClock.getTime();
			newNode.accessCount = 1;
			if (len < capacity) {
				setHead(newNode);
				map.put(key, newNode);
				len++;
			} else {
				// Evict based on UFCR utility score
				DoubleLinkedListNode minNode = null;
				double minUtility = Double.MAX_VALUE;
				
				DoubleLinkedListNode curr = head;
				while (curr != null) {
					double u = calculateUtility(curr);
					if (u < minUtility) {
						minUtility = u;
						minNode = curr;
					} else if (u == minUtility) {
						// Tie-breaker: oldest lastAccessTime (classic LRU)
						if (minNode == null || curr.lastAccessTime < minNode.lastAccessTime) {
							minNode = curr;
						}
					}
					curr = curr.next;
				}
				
				if (minNode != null) {
					System.out.println("UFCR Eviction: node " + minNode.key + " (Round " + (minNode.key/1000) + ") evicted with utility " + minUtility);
					map.remove(minNode.key);
					removeNode(minNode);
				} else {
					// Fallback to standard tail eviction
					System.out.println("UFCR Eviction Fallback: tail node " + end.key + " evicted");
					map.remove(end.key);
					end = end.pre;
					if (end != null) {
						end.next = null;
					}
				}
				
				setHead(newNode);
				map.put(key, newNode);
			}
		}
	}
	
	public int get_len(){
		return this.len;
	}
}
 
class DoubleLinkedListNode {
	public String val;
	public int key;
	public DoubleLinkedListNode pre;
	public DoubleLinkedListNode next;
	
	// UFCR metadata
	public double lastAccessTime;
	public int accessCount;
 
	public DoubleLinkedListNode(int key, String value) {
		val = value;
		this.key = key;
	}
}
