/* 
 * Copyright 2010 Aalto University, ComNet
 * Released under GPLv3. See LICENSE.txt for details. 
 */
package report;

import java.util.*;

import core.Application;
import core.ApplicationListener;
import core.DTNHost;
import core.SimClock;
import util.ContentDelivery;

public class CCNApplicationReport extends Report implements ApplicationListener {

	private int oppo_cache_hit=0;
	private int oppo_cache_miss=0;
	private int query_count=0;
	private int static_cache_hit=0;
	private int static_cache_miss=0;
	private int response_count=0;
	private int total_interval=0;
	private int num_got_response = 0;
	private int msg_forwarded = 0;
	private int response_from_other = 0;
	private int not_response = 0;
	private int res_found = 0;
	private int duplicated_query = 0;
	private int forwarding_Stop_l= 0;
	private int forwarding_Stop_p= 0;
	private int forwarding_Stop_n= 0;

	// ========== Caching Gain Index (CGI) ==========
	private int total_cache_hits = 0;
	private int total_gateway_fetches = 0;
	private double caching_gain_index = 0.0;

//	 ========== Content Accessibility Ratio (CAR) ==========
	private Set<String> unique_content_available = new HashSet<>();
	private Set<String> total_unique_content_cache = new HashSet<>();
	private double content_accessibility_ratio = 0.0;

	// ========== Retrieval Latency Reduction (RLR) ==========
	private double total_cache_hit_latency = 0.0;
	private int cache_hit_count_for_latency = 0;
	private double total_gateway_fetch_latency = 0.0;
	private int gateway_fetch_count_for_latency = 0;
	private double retrieval_latency_reduction = 0.0;

	// ========== Interest Satisfaction Rate (ISR) ==========
	private Set<String> uniqueInterests = new HashSet<>();
	private Set<String> uniqueDataPackets = new HashSet<>();
	private double interest_satisfaction_rate = 0.0;

	// Dissemination Efficiency
	//   1. Age of Information (AoI) = time from content creation
	//      to delivery. Lower AoI = fresher content.
	//   2. Overhead Ratio = total messages transmitted /
	//      unique content delivered
	private HashMap<String, Double> de_content_creation_time = new HashMap<>();;
	private List<ContentDelivery> de_deliveries = new ArrayList<ContentDelivery>();;
	private int de_total_messages_sent;
	private int de_unique_content_delivered;

	private List<MessageRecoder> msg_record = new ArrayList<MessageRecoder>();

	public class MessageRecoder{
		private String query_key = "";
		private double sentTime;
		private double receivedTime;
		private String hostName = "";
		private boolean gotResponse = false;


		public double getInterval(){
			return this.receivedTime - this.sentTime;
		}

		public MessageRecoder(){
			this.sentTime = 0.0;
			this.receivedTime = 0.0;
		}

		public String getQueryKey(){
			return this.query_key;
		}
		public void setQueryKey(String k){
			this.query_key = k;
		}

		public double getSentTime(){
			return this.sentTime;
		}
		public void setSentTime(double time){
			this.sentTime = time;
		}

		public double getReceivedTime(){
			return this.receivedTime;
		}
		public void setReceivedTime(double time){
			this.receivedTime = time;
		}

		public String getHostName(){
			return this.hostName;
		}
		public void setHostName(String name){
			this.hostName = name;
		}

		public boolean getGotResponse(){
			return this.gotResponse;
		}
		public void setGotResponse(boolean t){
			this.gotResponse = t;
		}
	}

	public void gotEvent(String event, Object params, Application app,
			DTNHost host) {
		if (event.equals("oppoCacheHit")) {
			this.oppo_cache_hit++;
			this.total_cache_hits++;
			total_unique_content_cache.add((String) params);
		}

		if (event.equals("forwardingStopList")) {
			this.forwarding_Stop_l++;
		}
		if (event.equals("forwardingStopListPIT")) {
			this.forwarding_Stop_p++;
		}
		if (event.equals("forwardingStopNonce")) {
			this.forwarding_Stop_n++;
		}
		if (event.equals("oppoCacheMiss")) {
			this.oppo_cache_miss++;
		}
		if (event.equals("SentQuery")) {
			this.query_count++;
			this.de_total_messages_sent++;
			uniqueInterests.add((String) params);

			de_content_creation_time.putIfAbsent((String)params, SimClock.getTime());

			MessageRecoder recorder = new MessageRecoder();
			recorder.setQueryKey((String)params);
			recorder.setSentTime(SimClock.getTime());
			recorder.setHostName(host.toString());

			msg_record.add(recorder);
		}
		if (event.equals("staticCacheHit")) {
			this.static_cache_hit++;
			this.total_cache_hits++;
			total_unique_content_cache.add((String) params);
		}
		if (event.equals("staticCacheMiss")) {
			//this.delays.add((Double)params);
			this.static_cache_miss++;
		}

		if (event.equals("OriginalGotResponse")) {
			this.response_count++;
			uniqueDataPackets.add((String) params);

			unique_content_available.add((String) params);

			int position = locate_query_key((String)params);
			if(position != -1){
				msg_record.get(position).setReceivedTime(SimClock.getTime());
				msg_record.get(position).setGotResponse(true);
				num_got_response ++;

				double latency = SimClock.getTime() - msg_record.get(position).getSentTime();

				total_gateway_fetch_latency += latency;
				gateway_fetch_count_for_latency++;
			}

			de_deliveries.add(new ContentDelivery((String) params, SimClock.getTime()));
			de_unique_content_delivered++;
		}
		if (event.equals("MsgForwarded")){
			this.msg_forwarded ++;
//			this.de_total_messages_sent++;
		}
		if (event.equals("GotResponse")) {
			this.response_from_other++;

//			int position = locate_query_key((String) params);
//			if (position != -1) {
//				double latency = SimClock.getTime() -
//						msg_record.get(position).getSentTime();
//
//				total_cache_hit_latency += latency;
//				cache_hit_count_for_latency++;
//			}
		}

		if (event.equals("NotFound")){
			this.not_response++;
		}

		if (event.equals("ResFound")){
			this.res_found++;
		}

		if (event.equals("SentDuplicatedQuery"))
		{
			this.duplicated_query++;
		}

// / /////////////////////////////
		if (event.equals("ContentCreated")) {
			if (params instanceof String) {
				String contentKey = (String) params;
//				total_unique_content_cache.add(contentKey);
//				de_content_creation_time.putIfAbsent(contentKey, SimClock.getTime());
			}
		}

		if (event.equals("ContentAvailable")) {
			if (params instanceof String) {
				String contentKey = (String) params;
//				unique_content_available.add(contentKey);
//				de_content_creation_time.putIfAbsent(contentKey, SimClock.getTime());
			}
		}

		// CacheHitLatency
		if (event.equals("CacheHitLatency")) {
			if (params instanceof Double) {
				double latency = (Double) params;
				this.total_cache_hit_latency += latency;
				this.cache_hit_count_for_latency++;
			}
		}

		//print state
		//print_state();

	}

	void print_state(){
		System.out.println("\r this.oppo_cache_hit = " + this.oppo_cache_hit);
		System.out.print("\r this.oppo_cache_miss = " + this.oppo_cache_miss);
	}

	public int locate_query_key(String key){
		for(MessageRecoder ms: msg_record){
			if(ms.getQueryKey().equals(key))
				return msg_record.indexOf(ms);
		}
		return -1;
	}



	public void calTotalInterval(){
		for(MessageRecoder ms : msg_record){
			if(ms.getGotResponse() == true){
				total_interval += ms.getInterval();
			}
		}
	}



	@Override
	public void done() {
		write("WebApp stats for scenario " + getScenarioName() +
				"\nsim_time: " + format(getSimTime()));

		calTotalInterval();
		if(num_got_response == 0){
			num_got_response = 1;
		}

		calculateCGI();
		calculateCAR();
		calculateRLR();
		calculateISR();

		String statsText =
			"\noppo_cache_hit: " + this.oppo_cache_hit +
			"\noppo_cache_miss: " + this.oppo_cache_miss +
			"\ndrop_list:  "		    + this.forwarding_Stop_l+
			"\ndrop_pit:  "		    + this.forwarding_Stop_p+
			"\ndrop_nonce:  "		    + this.forwarding_Stop_n+
			"\nquery_count: " + this.query_count +
			"\nduplicated_query: " + this.duplicated_query +
			"\nstatic_cache_hit: " + this.static_cache_hit +
			"\nstatic_cache_miss: " + this.static_cache_miss +
			"\nresponse_count: " + this.response_count +
			//"\nresource found: " + this.res_found +
			//"\nmsg_forwarded: " + this.msg_forwarded +
			"\naverage_interval: " + this.total_interval/this.num_got_response +
			"\ncaching_gain_index: " + String.format("%.2f", this.caching_gain_index) +
//			"\ncontent_accessibility_ratio: " + String.format("%.2f", this.content_accessibility_ratio) +
			"\nretrieval_latency_reduction: " + String.format("%.2f", this.retrieval_latency_reduction) +
			"\ninterest_satisfaction_rate: " + String.format("%.2f", this.interest_satisfaction_rate) +
			"\ndissemination_efficiency: " + String.format("%.6f", calculateDisseminationEfficiency())
			;

		write(statsText);
		super.done();
	}



//	CQI
	private void calculateCGI() {
		total_gateway_fetches = response_count;
		int total_successful_deliveries = total_cache_hits + total_gateway_fetches;
		if(total_successful_deliveries > 0) {
			caching_gain_index = (double) total_cache_hits / total_successful_deliveries * 100.0;
		}
	}
//  CAR
	private void calculateCAR() {
		System.out.println("Unique content gateway: "+unique_content_available.size() +" :: total unique content cache: " + total_unique_content_cache.size());
		if (total_unique_content_cache.size() > 0) {
			content_accessibility_ratio = (double) total_unique_content_cache.size()/unique_content_available.size();
		}
	}

	private void calculateRLR() {
		double avg_cache_latency = 0.0;
		double avg_gateway_latency = 0.0;

		if (cache_hit_count_for_latency > 0) {
			avg_cache_latency = total_cache_hit_latency / cache_hit_count_for_latency;
		}

		if (gateway_fetch_count_for_latency > 0) {
			avg_gateway_latency = total_gateway_fetch_latency / gateway_fetch_count_for_latency;
		}

		if (avg_gateway_latency > 0) {
			retrieval_latency_reduction = ((avg_gateway_latency - avg_cache_latency) / avg_gateway_latency) * 100.0;
		}
	}

	private void calculateISR() {
		int totalUniqueInterests = uniqueInterests.size();
		int totalUniqueData = uniqueDataPackets.size();

		if (totalUniqueInterests > 0) {
			this.interest_satisfaction_rate = ((double) totalUniqueData / totalUniqueInterests) * 100.0;
		}
	}

	public double calculateDisseminationEfficiency() {
		if (de_unique_content_delivered == 0) return 0.0;

		double totalAoI = 0.0;
		int validDeliveries = 0;

		for (MessageRecoder ms : msg_record) {
			if (ms.getGotResponse()) {
				double aoi = ms.getReceivedTime() - ms.getSentTime();
				System.out.println("received Time: "+ms.getReceivedTime() +"\t sent Time "+ms.getSentTime());
				if (aoi > 0) {
					totalAoI += aoi;
					validDeliveries++;
				}
			}
		}

		if (validDeliveries == 0) return 0.0;

		double avgAoI = totalAoI / validDeliveries;
		double overhead = (double) de_total_messages_sent / (double) de_unique_content_delivered;

		System.out.println("avgAoI: " + avgAoI
				+ " | overhead: " + overhead
				+ " | validDeliveries: " + validDeliveries);

		return (1.0 / avgAoI) / overhead;
	}
}
