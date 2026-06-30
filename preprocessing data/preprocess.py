import pandas as pd

input = "data/raw/ciciot23/ciciot23.csv"
output = "data/processed/ciciot23_9class.csv"

df = pd.read_csv(input)
print("Original Shape:", df.shape)

label_mapping = {
    "BenignTraffic": "Benign",

    # DDoS
    "DDoS-TCP_Flood": "DDoS",
    "DDoS-RSTFINFlood": "DDoS",
    "DDoS-UDP_Flood": "DDoS",
    "DDoS-ICMP_Flood": "DDoS",
    "DDoS-ACK_Fragmentation": "DDoS",
    "DDoS-SynonymousIP_Flood": "DDoS",
    "DDoS-PSHACK_Flood": "DDoS",
    "DDoS-SYN_Flood": "DDoS",
    "DDoS-UDP_Fragmentation": "DDoS",
    "DDoS-ICMP_Fragmentation": "DDoS",
    "DDoS-HTTP_Flood": "DDoS",
    "DDoS-SlowLoris": "DDoS",

    # DoS
    "DoS-UDP_Flood": "DoS",
    "DoS-TCP_Flood": "DoS",
    "DoS-SYN_Flood": "DoS",
    "DoS-HTTP_Flood": "DoS",

    # Mirai
    "Mirai-greeth_flood": "Mirai",
    "Mirai-udpplain": "Mirai",
    "Mirai-greip_flood": "Mirai",

    # Spoofing
    "MITM-ArpSpoofing": "Spoofing",
    "DNS_Spoofing": "Spoofing",

    # Recon
    "Recon-HostDiscovery": "Recon",
    "Recon-OSScan": "Recon",
    "Recon-PortScan": "Recon",
    "Recon-PingSweep": "Recon",
    "VulnerabilityScan": "Recon",

    # BruteForce
    "DictionaryBruteForce": "BruteForce",

    # WebAttack
    "BrowserHijacking": "WebAttack",
    "CommandInjection": "WebAttack",
    "SqlInjection": "WebAttack",
    "XSS": "WebAttack",
    "Uploading_Attack": "WebAttack",

    # Malware
    "Backdoor_Malware": "Malware"
}

df["label"] = df["label"].map(label_mapping)
print("\nMapped Class Counts:")
print(df["label"].value_counts())

targets = {
    "Benign": 500000,
    "DDoS": 500000,
    "DoS": 500000,
    "Mirai": 500000
}

final_parts = []
for cls in [
    "Benign",
    "DDoS",
    "DoS",
    "Mirai",
    "Spoofing",
    "Recon",
    "BruteForce",
    "WebAttack",
    "Malware"
]:

    cls_df = df[df["label"] == cls]
    if cls in targets:
        cls_df = cls_df.sample( n=targets[cls], random_state=42)
    final_parts.append(cls_df)
    print(f"{cls}: {len(cls_df):,}")

final_df = pd.concat(final_parts)
final_df = final_df.sample(frac=1,random_state=42).reset_index(drop=True)

print("\nFinal Shape:", final_df.shape)
print("\nFinal Distribution:")
print(final_df["label"].value_counts())

final_df.to_csv(output,index=False)
print(f"\nSaved to: {output}")
