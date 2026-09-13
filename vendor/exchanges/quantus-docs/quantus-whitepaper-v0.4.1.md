# Quantus Whitepaper | Quantum Security - v0.4.1

- Path: /whitepaper/v0.4.1/
- Generated: 2026-09-10T06:07:31.923Z

## Extracted Content

[](/)

*   [Technology](/technology/)
*   [Wallet](/wallet/)
*   [Blog](/blog/)
*   [Community](/community/)
*   [Docs](https://docs.quantus.com/)
*   [Q-Day Checker](/quantum-risk-checker/)

[Download Wallet](#)

[Technology](/technology/) [Wallet](/wallet/) [Blog](/blog/) [Community](/community/) [Docs](https://docs.quantus.com/) [Q-Day Checker](/quantum-risk-checker/)

[Download Wallet](#)

Whitepaper / V0.4.1

Quantus

quantum secure, encrypted money

Published

September 9, 2026

Version

0.4.1

Classification

Public

![Decoration](/whitepaper/v0.3.3/whitepaper-cover-decoration.webp)

# Quantus Whitepaper

Authors: [Christopher Smith](/team/christopher-smith) , [Jonathan Angle](/team/jonathan-angle)

|

Last updated: September 9, 2026

v0.4.1 Latest

*   [v0.4.1 Latest Sep 2026](/whitepaper)

On this page

*   [Legal Disclaimer](#legal-disclaimer)
*   [Contents](#contents)
*   [Introduction](#chapter-01)
*   [The Quantum Threat](#the-quantum-threat)
*   [Unique Value Proposition](#unique-value-proposition)
*   [The Quantum Threat to Blockchain](#chapter-02)
*   [Quantum Computing Basics](#quantum-computing-basics)
*   [The Shrinking Timeline](#the-shrinking-timeline)
*   [Four Threat Categories](#four-threat-categories)
*   [Scaling Challenges in Post-Quantum Cryptography](#scaling-challenges-in-post-quantum-cryptography)
*   [TPS vs QTPS](#tps-vs-qtps)
*   [The Migration Crisis](#chapter-03)
*   [The Coordination Problem](#the-coordination-problem)
*   [The Migration Timeline Problem](#the-migration-timeline-problem)
*   [The Lost Coin Problem](#the-lost-coin-problem)
*   [Quantus Architecture](#chapter-04)
*   [Foundation](#foundation)
*   [Quantum Secure](#quantum-secure)
*   [Private](#private)
*   [Scalable](#scalable)
*   [Money](#money)
*   [Account Security](#chapter-05)
*   [HD-Lattice](#hd-lattice)
*   [Check-Phrases](#check-phrases)
*   [Multisig Accounts](#multisig-accounts)
*   [Advanced Accounts](#advanced-accounts)
*   [Tokenomics and Governance](#chapter-06)
*   [Block Rewards](#block-rewards)
*   [Investor and Team Allocation](#investor-and-team-allocation)
*   [Company Allocation](#company-allocation)
*   [Transaction Fees](#transaction-fees)
*   [Network Upgrades](#network-upgrades)
*   [Governance System](#governance-system)
*   [Roadmap](#chapter-07)
*   [Risks](#chapter-08)
*   [Implementation Issues](#implementation-issues)
*   [NIST Algorithm Selection Issues](#nist-algorithm-selection-issues)
*   [Quantum Computing Timelines](#quantum-computing-timelines)
*   [Other Considerations](#other-considerations)
*   [References & Further Reading](#chapter-09)
*   [Further Reading](#further-reading)

## Legal Disclaimer

_This whitepaper is provided for informational purposes only and does not constitute an offer to sell, a solicitation of an offer to buy, or a recommendation for any security, investment, or financial product. Readers should conduct their own due diligence and consult with qualified professionals before making any investment decisions. Quantus makes no representations or warranties regarding the accuracy or completeness of the information herein._

## Contents

2.  [01
    
    Introduction
    
    ](#chapter-01)

4.  [02
    
    The Quantum Threat to Blockchain
    
    ](#chapter-02)

6.  [03
    
    The Migration Crisis
    
    ](#chapter-03)

8.  [04
    
    Quantus Architecture
    
    ](#chapter-04)

10.  [05
     
     Account Security
     
     ](#chapter-05)

12.  [06
     
     Tokenomics and Governance
     
     ](#chapter-06)

14.  [07
     
     Roadmap
     
     ](#chapter-07)

16.  [08
     
     Risks
     
     ](#chapter-08)

18.  [09
     
     References & Further Reading
     
     ](#chapter-09)

  

## 01 Introduction

### The Quantum Threat

Traditional blockchains face an existential threat from cryptographically relevant quantum computers (CRQCs). The cryptographic foundations of blockchains rely on the hardness of the discrete logarithm problem (DLP), and quantum algorithms, notably Shor’s, can solve the DLP exponentially faster than classical computers. This vulnerability could enable quantum adversaries to derive private keys from public keys, which would allow them to forge transactions and decrypt sensitive financial data.

Over the coming years, trillions of dollars in blockchain-secured value will have to migrate to:

*   Post-quantum solutions on existing blockchains (no complete solutions of material size currently exist)
*   Post-quantum blockchains (Quantus)
*   Out of crypto and into other asset classes (gold, fiat, real estate)

> Without proactive quantum-resistant solutions, the trillion-dollar crypto economy risks sudden devaluation.

### Unique Value Proposition

Named after the Latin word for “how much”, Quantus is quantum secure, private, scalable money: peer-to-peer electronic cash built for the quantum era.

Why does the industry need another L1?

There are currently no other blockchain assets that satisfy all four criteria: quantum secure, private, scalable, money.

Quantus is not a general purpose smart contract platform. It is more like Bitcoin, Monero, or Zcash and less like Ethereum or Solana.

Like a restaurant with a few highly perfected menu items, Quantus delivers:

*   Post-quantum signatures for all transactions (ML-DSA)
*   Post-quantum authentication and encryption (ML-DSA and ML-KEM) to secure peer connections
*   Post-quantum zero-knowledge proofs for private transactions and scaling
*   Clear signing on all transactions and cold storage support for simple, high-security self custody
*   Multisig addresses, human-readable check-phrases, and an advanced account type with security features that deter theft
*   21,000,000 supply cap and Proof-of-Work consensus to ensure sound money, security, and scarcity

The decision to focus on quantum secure, private, scalable money stems from the threat CRQCs present to the industry and Bitcoin’s inability to address these challenges.

## 02 The Quantum Threat to Blockchain

### Quantum Computing Basics

Quantum computers leverage principles like superposition and entanglement to perform computations that are intractable for classical machines. Unlike classical bits, which are either 0 or 1, quantum bits (qubits) can exist in multiple states simultaneously, enabling exponential parallelism for certain problems. This capability poses existential risks to the cryptographic systems underpinning blockchains, as algorithms developed for quantum hardware undermine the security assumptions of most pre-quantum public-key cryptography.

**Shor’s algorithm**, introduced in 1994 by Peter Shor, provides a polynomial-time method for factoring large integers and solving the discrete logarithm problem on a quantum computer. It exploits Quantum Fourier Transforms (QFT) to find the period of a function, allowing efficient reversal of the trapdoor functions that underlie schemes like RSA or elliptic curve cryptography (ECC). For blockchain finance, this means an attacker with a sufficiently powerful quantum computer (estimated at 1,200 to 1,450 logical qubits [\[11\]](#reference-11) , down from earlier estimates of roughly 2,000 [\[6\]](#reference-6) [\[7\]](#reference-7) [\[8\]](#reference-8) [\[9\]](#reference-9) ) could derive private keys from public keys in polynomial time O(n³), an extreme speed-up rendering vulnerable systems obsolete overnight. [\[1\]](#reference-1) Researchers keep revising this figure down as hardware and algorithms improve.

**Grover’s algorithm**, proposed by Lov Grover in 1996, offers a quadratic speedup for unstructured search problems, reducing search time from O(n) to O(√n) operations. While not as devastating as Shor’s for asymmetric cryptography, Grover’s impacts symmetric primitives like hash functions and AES encryption, effectively halving the security level (e.g., a 256-bit key behaves like 128 bits against quantum attacks). This attack is mitigated by simply doubling the security bits, rather than changing the cryptographic scheme. Additionally, Grover’s quadratic speedup is impractical due to its high qubit and gate requirements, requiring billions of sequential operations with limited parallelization, making it infeasible for real-world reversals even on future hardware. [\[2\]](#reference-2)

### The Shrinking Timeline

Resource estimates for breaking pre-quantum cryptography keep falling. In March 2026, Google cut its estimate to under 500,000 physical qubits to break a 256-bit elliptic-curve key, a 20x reduction from the previous best estimate. [\[11\]](#reference-11) In June 2026, Eigen Labs opened [ecdsa.fail](https://ecdsa.fail), a public leaderboard where researchers and AI agents compete to shrink the circuit that breaks secp256k1, the curve under every Bitcoin and Ethereum signature. The open effort matched Google’s result in eight hours and beat it within three days. [\[20\]](#reference-20)

NIST has formalized the transition away from vulnerable schemes, deprecating RSA and 256-bit elliptic-curve cryptography by 2030 and disallowing them entirely by 2035. [\[12\]](#reference-12) In June 2026, Executive Order 14412 moved the federal deadline from 2035 to December 31, 2030 for key establishment and December 31, 2031 for digital signatures, with a pilot migration to complete by the end of 2027. [\[13\]](#reference-13)

No one knows when a cryptographically relevant quantum computer will arrive, but it could arrive within five years. Anything that must stay secret longer than that already needs post-quantum encryption. The information security industry has acted on this: Signal added post-quantum key exchange in 2023, Apple added it to iMessage in 2024, and Cloudflare now serves most of its traffic over hybrid post-quantum TLS. [\[14\]](#reference-14) [\[15\]](#reference-15) [\[16\]](#reference-16)

### Four Threat Categories

#### 01 - Forging Digital Signatures

Shor’s algorithm directly threatens ECC-based signatures used in most blockchains (e.g., Bitcoin’s secp256k1 curve), allowing adversaries to authorize fraudulent transactions. This would be a critical failure of the most basic feature of a blockchain.

#### 02 - Forging False Proofs in Zero-Knowledge Systems

Many zero-knowledge proofs, such as those in zk-SNARKs for privacy-focused finance, rely on discrete logarithm hardness via elliptic-curve pairings for commitments. Shor’s could enable the creation of invalid proofs that appear valid, which could allow an attacker to mint new coins or falsify the state of Layer 2s (L2s).

#### 03 - Decrypting Secret Information

Quantum attacks could expose encrypted data protected by vulnerable public-key schemes in privacy protocols. It could also decrypt p2p communications in financial protocols, revealing sensitive details and enabling targeted theft.

#### 04 - Reversing Hash Functions

Grover’s algorithm could accelerate preimage attacks on hashes like SHA-256, used for proof-of-work and address generation, but this is the least concerning threat. Many post-quantum cryptographic schemes incorporate hash-based constructions as hashes are considered secure enough with a large enough digest.

### Scaling Challenges in Post-Quantum Cryptography

While post-quantum cryptography (PQC) offers essential protections against quantum threats, it introduces significant scaling hurdles due to the inherent design of these algorithms. Unlike elliptic curve schemes, which rely on compact mathematical structures, PQC primitives require larger parameters to maintain security against both classical and quantum adversaries. This results in substantially bigger public keys, private keys, and signatures, often by many orders of magnitude. The following table illustrates typical sizes for ML-DSA compared to classical counterparts like 256-bit ECDSA: [\[10\]](#reference-10)

ALGORITHM

PUBLIC KEY

PRIVATE KEY

SIGNATURE

ML-DSA-87 (Dilithium)

2,592 bytes

4,896 bytes

4,627 bytes

ML-DSA-65 (Dilithium)

1,952 bytes

4,032 bytes

3,309 bytes

ECDSA (256-bit)

32 bytes

32 bytes

65 bytes

ML-DSA-87 (Dilithium)

PUBLIC KEY 2,592 bytes

PRIVATE KEY 4,896 bytes

SIGNATURE 4,627 bytes

ML-DSA-65 (Dilithium)

PUBLIC KEY 1,952 bytes

PRIVATE KEY 4,032 bytes

SIGNATURE 3,309 bytes

ECDSA (256-bit)

PUBLIC KEY 32 bytes

PRIVATE KEY 32 bytes

SIGNATURE 65 bytes

As shown, ML-DSA signatures can be over 70 times larger than ECDSA equivalents, and public keys more than 80 times larger. Other PQC families exacerbate this: hash-based schemes like SPHINCS+ may produce signatures up to 41 KB, while even size-optimized lattice variants like FALCON still exceed classical sizes by a significant multiple.

In a blockchain context, these inflated sizes compound into systemic scaling issues. Larger signatures bloat individual transactions, reducing throughput as blocks fill faster and require more time for validation. This also strains peer-to-peer (P2P) communication, increasing bandwidth demands and propagation delays, which can heighten the risk of network forks or orphaned blocks in consensus mechanisms like proof-of-work. Storage requirements are also affected, leading to higher node operating costs and barriers for participation, especially for resource-constrained users or validators.

### TPS vs QTPS

“TPS” is an industry term that measures how many transactions a blockchain can process per second. Quantum-secure transactions per second (QTPS) measures the theoretical throughput of a blockchain if every transaction used its available post-quantum address type and transaction signatures.

A chain with no post-quantum address type has a QTPS of zero.

If Bitcoin added ML-DSA-65 with no change to block size or rate, a simple transaction would be a 3,309-byte signature and a 1,952-byte public key instead of 72 and 33 bytes today. A block would hold about 690 such transactions instead of about 6,000, and Bitcoin’s QTPS would be about 1.1, down from ~10 TPS.

NOTE

These scaling challenges will have to be addressed by all blockchains in the future. Bitcoin, for example, will have about 1 QTPS or less if the max block size is not increased.

## 03 The Migration Crisis

### The Coordination Problem

Bitcoin’s conservative culture resists protocol changes. Any PQC upgrade would require consensus on contentious issues such as migration timelines, potential coin seizure, and block size increases. Even if the community agreed, every individual user would need to migrate their coins to new quantum-secure addresses. Migration requires action from every crypto holder, many of whom have lost access to their wallets or remain unaware of the threat.

These issues are uniquely challenging to Bitcoin due to its lack of clear leadership and philosophy of technical ossification.

Agreement is the first step. After Bitcoin ships a post-quantum address type, migration can begin.

### The Migration Timeline Problem

Each chain’s clock starts when it ships a post-quantum address type and ends on the day a cryptographically relevant quantum computer exists.

Once the address type ships, every holder must generate a post-quantum key pair and move their coins to it. Bitcoin has about 170 million unspent outputs, and each one needs its own signature to move. [\[17\]](#reference-17) If migration used every byte of every block, moving them all would take at least 80 days. Migration will not get every byte. Holders who have already migrated keep transacting, and their post-quantum signatures are 20x to 80x larger than ECDSA, so each post-quantum transaction uses more block space than a transaction today. Many holders will send a test transaction first.

Under the most optimistic assumptions, with every holder informed and acting promptly, migration takes months. SegWit, a far smaller change with no deadline, took two years to reach half of Bitcoin transactions. [\[18\]](#reference-18) Realistically, the migration will take years, and every unmigrated coin is exposed.

### The Lost Coin Problem

An estimated 2.3 to 3.7 million Bitcoin, over a tenth of the total supply, is permanently inaccessible due to lost keys, deceased holders, or forgotten wallets. [\[3\]](#reference-3) These coins cannot be migrated and serve as a public bounty for creating a cryptographically relevant quantum computer (CRQC).

> The only technical solution requires a hard deadline that freezes unmigrated coins.

In June 2026, Binance founder Changpeng Zhao proposed roughly a one-year window after a post-quantum upgrade, after which a fork would freeze coins left in vulnerable addresses, including the 1.1 million BTC attributed to Satoshi. The proposal split the industry. [\[19\]](#reference-19)

QUANTUS'S ANSWER

These compounding challenges make retrofitting quantum security onto existing chains extraordinarily difficult. Quantus sidesteps this by supporting only post-quantum address types.

## 04 Quantus Architecture

### Foundation

Quantus is built on Substrate, a blockchain SDK developed by Parity Technologies, the team behind Polkadot. Substrate is highly modular, enabling easy replacement of components so we can focus on what makes Quantus unique.

Quantus upgrades Substrate by:

*   Adding support for post-quantum signature schemes
*   Upgrading the p2p networking security to be post-quantum
*   Adding the zk-tree, a Poseidon2 Merkle tree of every balance credit, committed in each block header so wallets can prove deposits inside zero-knowledge proofs

### Quantum Secure

#### Post-Quantum Cryptographic Primitives

Quantus employs NIST-standardized PQC to ensure the security of transactions and network communications against quantum threats. At the core of transaction integrity is **ML-DSA** (Module-Lattice-based Digital Signature Algorithm, formerly known as CRYSTALS-Dilithium), a lattice-based signature scheme selected for its balance of security, efficiency, and ease of implementation. ML-DSA leverages the hardness of problems like Learning With Errors (LWE) and Short Integer Solution (SIS) over module lattices, providing robust resistance to both classical and quantum attacks, including those from Shor’s algorithm. [\[4\]](#reference-4)

For transaction signatures, Quantus supports two ML-DSA parameter sets. ML-DSA-65 (NIST Security Level 3) is the primary scheme and the default in Quantus wallets, offering a strong balance of security and signature size. ML-DSA-87, the parameter set offering the highest security level (NIST Security Level 5, equivalent to AES-256), is also supported for users who want the maximum margin against potential cryptanalytic breakthroughs in lattice problems. Lattice cryptography is relatively new and less battle-tested than classical schemes, and the larger parameters mitigate risks from potential advances in lattice cryptanalysis.

#### Alternatives Considered

ML-DSA was selected over alternatives like FN-DSA (Falcon) due to FN-DSA’s greater implementation complexity (e.g., requiring floating-point operations, which are blockchain-unfriendly), lack of deterministic key generation in its specification, and its non-finalized status at the time of development.

Hash-based options like SLH-DSA were not chosen because of their even larger signature sizes (exceeding 17 KB). Crypto-agility (being able to swap in different signature schemes) is built into Substrate, so it is relatively easy to add these alternatives at a future date, should circumstances demand.

While ML-DSA results in larger keys and signatures, these are manageable in Quantus’s early-stage network, where storage is not yet a bottleneck, and optimizations like wormhole addresses via zero-knowledge proofs will address scaling.

For technical details about the implementation see [QIP-0006](https://github.com/Quantus-Network/improvement-proposals/blob/main/qip-0006.md).

#### litep2p - Quantum-Secure Networking

Quantus secures peer-to-peer (P2P) node communications using a combination of ML-DSA for authentication and **ML-KEM** (Module-Lattice-based Key Encapsulation Mechanism, formerly CRYSTALS-Kyber) for encryption. This integration extends PQC to the litep2p networking stack, modifying core components for quantum resistance: using ML-DSA-87 signatures for peer identity and ML-KEM-768 for transport security over the four-message pqXX Noise pattern in which every key exchange is a KEM encapsulation, with no Diffie-Hellman fallback. [\[5\]](#reference-5)

The P2P layer is often neglected in quantum-security analysis. Authentication of peers is important, but the worst an attacker could do at the peer level is impersonate a node and send invalid messages, which could result in denial-of-service. This attack is already mitigated by the fact that nodes are generally untrusted in the blockchain model and nodes can easily switch their keys if the attack is detected. Likewise, decrypting P2P communications yields limited attacker benefits (e.g., tracking transaction paths, mitigated by proxies or Tor), and most data becomes public onchain anyway.

Nevertheless, quantum-securing the P2P layer protects against eavesdropping, man-in-the-middle attacks, and quantum decryption, ensuring that node gossip, block propagation, and other network interactions remain confidential and tamper-proof for the foreseeable future.

For technical details about the implementation see [QIP-0004](https://github.com/Quantus-Network/improvement-proposals/blob/main/qip-0004.md).

### Private

#### Two Address Types

Quantus has two address types. A transparent address is the hash of an ML-DSA public key; its balance and every transfer in and out are visible onchain. An encrypted address is a wormhole address: coins sent to it are provably burned, and the owner later mints them at any exit address with a zero-knowledge proof that references no source. The two are interoperable, and the chain cannot tell them apart: a deposit into an encrypted address is an ordinary transfer, and the address holds an ordinary visible balance.

#### Wormhole Addresses

To address the scaling challenges inherent in post-quantum cryptography, Quantus introduces an innovative aggregated post-quantum signature scheme called **“Wormhole Addresses”**. This system leverages zero-knowledge proofs (ZKPs) generated via the Plonky2 proving system (basically STARKs) to move balance verification off-chain, allowing the chain to verify a single compact proof without processing individual signatures. The chain itself verifies every proof layer. Quantus has no L2.

Wormhole Addresses enable the verification of a large number of transactions with one proof, with the public inputs (e.g., nullifiers, exit addresses, and amounts) becoming the primary limiting factor. This reduces the amortized per-transaction footprint to a small constant, far below any known PQC signature scheme.

The quantum security of the scheme derives from FRI (Fast Reed-Solomon Interactive Oracle Proofs) commitments built on the Poseidon hash family, instead of the quantum-vulnerable elliptic-curve pairings commonly used in SNARKs. Additionally the authentication secrets are hidden behind **Poseidon2**. Since secure hash functions are only quadratically weakened by Grover’s algorithm, not broken, hash preimage proofs can serve as lightweight post-quantum signatures in ZK contexts, similar to hash-based schemes like SPHINCS+.

#### Privacy Properties

Beyond scaling, wormhole transfers function as Quantus’s encrypted transactions, and an address that receives funds this way functions as an encrypted account. The chain does not distinguish wormhole addresses from ordinary addresses: a deposit is an ordinary transfer, and the receiving address shows a normal, visible balance onchain. Spending works differently. Exiting the wormhole mints funds at the exit address against a zero-knowledge proof whose public inputs contain only nullifiers, a recent block hash, amounts, and exit addresses. Nothing onchain references the source address, and the source balance is never debited. To an observer, funds received through a wormhole address appear to remain exactly where they are, whether or not they have since been spent. An encrypted send breaks the onchain link between sender and receiver. Wallets expose this as two transaction modes, transparent and encrypted, with proofs generated locally on the user’s device.

An observer who matches a deposit to an exit of the same amount at a suggestive time can narrow the link between them. Wallets batch up to seven exits into one proof and pad the batch with dummy slots. Encrypted transfers move in steps of 0.01 QTC, so many transfers share the same amount. Every native transfer joins the same anonymity set. Mining-reward wormhole addresses are identifiable by construction.

#### Client / Prover Flow

Users generate a provably unspendable address by double-hashing a salt concatenated with a secret:

```
H(H(salt|secret))
```

This construction prevents false positives (e.g., mistaking a single-hash public key for an unspendable address) because in Substrate (and generally) blockchain addresses are the single hash of a public key, which is derived from the private key via some algebraic operation, not via a secure hash. The security of the construction therefore reduces to finding the preimage-of-a-preimage of a secure hash. Tokens sent to this address are effectively burned. They cannot be spent because no private key exists for the address that received them. These coins can therefore be re-minted without inflating supply.

The zk-tree records every balance credit on the chain as a leaf holding the recipient, a per-recipient transfer count, and the amount. The user’s wallet opens a Merkle proof from a recent block header’s zk-tree root to the leaf for its deposit. A nullifier is computed to prevent double-spends:

```
H(H(salt | secret | transfer_count))
```

#### Aggregator Flow

Aggregation uses Plonky2’s recursion in two layers, where each parent proof verifies its child proofs and passes their public inputs upward.

In the first layer, the user’s wallet batches up to seven of its own leaf proofs into one private batch. The circuit shuffles the slots, pads empty ones with dummy proofs so an observer cannot tell how many are real, requires every real leaf to reference the same recent block hash, deduplicates exit addresses within the batch, and sums their amounts. Nullifiers pass through unchanged.

In the second layer, any party (a miner or a professional aggregator) batches up to 53 private batches into one public batch and earns part of the fee. This layer forwards each private batch’s exits and nullifiers exactly as they are, with no further summing or deduplication. Each private batch stays a separate settlement segment, so if one contains an already-spent nullifier, the chain rejects only that segment and settles the rest.

#### Chain / Verifier Flow

The network verifies the aggregated proof by checking: block hash is onchain and recent, nullifier uniqueness (to prevent double-spends), and proof validity. The ZK circuit enforces zk-tree Merkle proof correctness, nullifier computation accuracy, address unspendability, that outputs plus fee do not exceed the input, and block header linkage.

#### Why Plonky2

*   Formally verified in part (Quantus circuits and a subset of Plonky2)
*   Post-quantum
*   No trusted setup
*   Efficient proving/verification
*   Seamless proof aggregation
*   Rust-native implementation
*   Compatible with Substrate’s no-std environment

#### Security Notes

Potential risks include inflation bugs from faulty circuit/verification implementations. Users can optionally prove an address is a wormhole by publishing the first hash without revealing the secret. Verification transactions are unsigned, so the chain limits denial-of-service non-financially: cheap checks at pool admission, full proof verification only at dispatch, and a 512 KiB proof size cap. Exits mint balances without raising total issuance, since the deposited coins were provably burned, so the supply cap is unaffected.

For more technical details about the implementation see [QIP-0005](https://github.com/Quantus-Network/improvement-proposals/blob/main/qip-0005.md).

### Scalable

Every transaction on Quantus is post-quantum, so its TPS and QTPS are the same number. Block space bounds throughput: the target block time is 12 seconds and each block allows 3.75 MB of transactions.

MODE

BYTES PER TRANSFER

TRANSFERS PER BLOCK

QTPS

Transparent, ML-DSA-87

~7.3 KB

~510

~43

Transparent, ML-DSA-65

~5.4 KB

~690

~58

Encrypted, current two-layer aggregation

~266 KB per 371 transfers

~5,200

~430

Encrypted, theoretical ceiling

~112 bytes of public inputs

~33,000

~2,800

Transparent, ML-DSA-87

BYTES PER TRANSFER ~7.3 KB

TRANSFERS PER BLOCK ~510

QTPS ~43

Transparent, ML-DSA-65

BYTES PER TRANSFER ~5.4 KB

TRANSFERS PER BLOCK ~690

QTPS ~58

Encrypted, current two-layer aggregation

BYTES PER TRANSFER ~266 KB per 371 transfers

TRANSFERS PER BLOCK ~5,200

QTPS ~430

Encrypted, theoretical ceiling

BYTES PER TRANSFER ~112 bytes of public inputs

TRANSFERS PER BLOCK ~33,000

QTPS ~2,800

### Money

#### Consensus Mechanism

Quantus uses a Proof-of-Work (PoW) consensus algorithm that preserves the desirable properties of Bitcoin’s consensus algorithm while improving compatibility with ZK-proof systems by switching out SHA-256 with **Poseidon2**. The target block time is 12 seconds.

Importantly, this change is not being made for quantum security. Cryptographic hash functions like SHA-256 are weakened but not destroyed by quantum algorithms, notably Grover’s. Some post-quantum signature schemes use secure hashes as a building block for this reason.

Poseidon2 is a refinement of the Poseidon hash function. Creating SNARKs or STARKs for computations involving traditional hash functions like SHA-256 often requires nearly 100x the number of gates compared to using Poseidon, which relies entirely on algebraic functions over field elements, instead of bit-level operations.

We use the **Goldilocks field** for both Poseidon2 and Plonky2. The Goldilocks field’s order fits in an unsigned 64-bit integer, which increases efficiency without compromising soundness.

Supply is capped at 21,000,000 QTC. See section 06.

## 05 Account Security

There are many risks in managing cryptocurrency keys. Most of them are avoidable.

### HD-Lattice

Hierarchical Deterministic (HD) wallets are the industry standard for blockchains, allowing users to back up one seed phrase for all keys, improving security and convenience over manual backups per action. Adapting this to lattice schemes like Dilithium involves two challenges:

*   HMAC-SHA512 outputs can’t directly form lattice private keys, which are polynomials sampled from a ring with certain properties.
*   Non-hardened key derivation relies on elliptic curve addition, absent in lattices (public keys aren’t closed under any algebraic operation).

Quantus addresses the first issue by using the output of the HMAC as entropy to deterministically construct the private key, not as the private key itself. The second issue is less critical and remains an open research question whether lattice cryptography can be adapted to address it.

Transparent account keys and wormhole secrets derive from the same seed on separate paths (BIP44 coin types 189189’ and 189189189’), so one seed phrase backs up both address types.

For more technical details see [QIP-0002](https://github.com/Quantus-Network/improvement-proposals/blob/main/qip-0002.md).

### Check-Phrases

Quantus introduces “check-phrases,” a cryptographically secure human-readable checksum for blockchain addresses. The address is hashed to generate a short sequence of memorable words from the BIP-39 mnemonic list. Check-phrases protect against typos, tampering, and address poisoning attacks. A 40,000-iteration key derivation function makes rainbow table attacks expensive. For large transactions, users should still verify every character of the address. A check-phrase is a checksum, not an address. It cannot receive funds.

For more technical details see [QIP-0008](https://github.com/Quantus-Network/improvement-proposals/blob/main/qip-0008.md).

### Multisig Accounts

A multisig account starts as a new account. The creator lists the signers (up to 100), sets how many of them must approve a transaction (the threshold), and picks a nonce, and the chain derives the account’s address from those three things. The signers and threshold never change, because they are part of the address. Anyone who wants a different set creates a new multisig and moves the funds. Any signer can propose a transaction. Once the threshold of signers approve, it executes. Proposals expire after at most two weeks.

Multisig accounts are native to the chain. They are transparent addresses. A multisig cannot be an encrypted address, and an encrypted address cannot be a signer. A multisig can send to and receive from encrypted addresses, and it can be a guardian for an advanced account.

### Advanced Accounts

Advanced accounts are for users who want more protection than a single key. They exist only for transparent addresses, and most users never need one. Any transparent account can become an advanced account. The upgrade is permanent, so a thief cannot switch it off. The owner names a **guardian**: another account, preferably better secured than the advanced account itself, such as a hardware wallet, a multisig, or a trusted third party. The guardian cannot spend from the account. It can only cancel the account’s pending transfers and recover its funds.

The guardian, the mandatory time lock, and key recovery exist only for advanced accounts and are optional. The owner sets these parameters once, when creating the account, and cannot change them afterward. An owner who wants different parameters creates a new advanced account and moves the funds there.

These features are built for exchanges, custodians, and other advanced users. Most people will never see them.

Guardians can be chained: an advanced account’s guardian can itself be an advanced account with its own guardian. This creates composable hierarchies where each guardian has superior permissions to the account it protects. The design gives users time to detect and respond to unauthorized activity without compromising finality for legitimate transfers.

For more technical details see [QIP-0011](https://github.com/Quantus-Network/improvement-proposals/blob/main/qip-0011.md).

#### Time-Locked Transactions

Any transparent account can attach a delay to an outgoing transfer, during which the sender can cancel it. This corrects mistakes and deters theft without sacrificing finality.

An advanced account can set a mandatory delay on every outgoing transfer. Only the guardian can cancel, and cancelled funds go to the guardian.

For more technical details see [QIP-0009](https://github.com/Quantus-Network/improvement-proposals/blob/main/qip-0009.md) and [QIP-0010](https://github.com/Quantus-Network/improvement-proposals/blob/main/qip-0010.md).

#### Key Recovery

Many crypto-fortunes have gone to the grave with their owners. Advanced accounts offer a way out. Upon the creation of an advanced account, the owner names a guardian who can recover all of the account’s funds at any time. An owner who names an heir’s account, a family multisig, or a professional custodian as guardian has an onchain will that needs no court.

## 06 Tokenomics and Governance

Quantus has a fixed monetary policy: a 21,000,000 QTC supply cap, an exponentially decaying emission curve, and a transaction fee burn that keeps the block reward above zero indefinitely while maintaining the supply cap.

### Block Rewards

Quantus employs a straightforward block emission imitating that of Bitcoin, but with a smooth decay rather than choppy halvings. A simple heuristic determines the reward each block:

```
block_reward = (max_supply - current_supply) / 50,000,000
```

This heuristic forms a smooth exponentially decaying curve as the block\_reward contributes to the current\_supply which reduces the block\_reward computed at the next block. Any burns from fees reduce current\_supply and become part of the budget for block rewards.

### Investor and Team Allocation

Quantus was built with the help of investors who took great risk in funding it. At genesis, there is a one-time mint of 27% of the total supply (5,670,000 QTC). The remaining 73% (15,330,000 QTC) can only be mined into existence. There is no dev tax: miners keep full block rewards.

The investors, founders, and team own 23% of total supply. These tokens stay locked for the first year after mainnet, then vest linearly over the following 36 months, enforced onchain by a dedicated vesting pallet.

### Company Allocation

The company holds 4% of total supply. 1% is liquid at genesis to seed initial liquidity. The remaining 3% is for funding future company operations, locked for the first year after mainnet, then vesting linearly over the following 36 months.

### Transaction Fees

Every transaction fee goes to miners or is burned.

TRANSACTION TYPE

FEE

DESTINATION

Transparent, ML-DSA-65 (default)

About 0.0062 QTC per simple transfer, plus an optional tip

Miners

Transparent, ML-DSA-87

About 0.0081 QTC per simple transfer, plus an optional tip

Miners

Encrypted

0.04% of the amount, minimum 0.01 QTC

Half to miners, half burned

Advanced account cancellation (rare, advanced accounts only)

1% of the cancelled amount

Burned

Transparent, ML-DSA-65 (default)

FEE About 0.0062 QTC per simple transfer, plus an optional tip

DESTINATION Miners

Transparent, ML-DSA-87

FEE About 0.0081 QTC per simple transfer, plus an optional tip

DESTINATION Miners

Encrypted

FEE 0.04% of the amount, minimum 0.01 QTC

DESTINATION Half to miners, half burned

Advanced account cancellation (rare, advanced accounts only)

FEE 1% of the cancelled amount

DESTINATION Burned

In practice, encrypted transactions of 25 QTC or less pay the flat 0.01 QTC minimum; anything larger pays the 0.04% fee.

As long as there is activity on the network, this fee structure pays miners to secure it in perpetuity. Quantus keeps a hard cap of 21,000,000 QTC without ever running out of security budget.

### Network Upgrades

Quantus supports “forkless” upgrades through Substrate’s runtime upgrades, allowing the blockchain’s core logic (the “runtime”) to evolve without hard forks that could disrupt the network. This upgrade path minimizes downtime and risk, so security fixes and cryptographic upgrades ship without a hard fork.

As the community gains confidence in the system over time, the power to change the runtime will be significantly reduced.

### Governance System

A monetary system that users depend on should be stable, predictable, and secure.

The **Technical Collective** is a curated group of technical experts serving as a specialized body to propose, review, or whitelist urgent technical matters, expediting them through a dedicated track while maintaining community oversight. It has no mandate to change the network’s monetary policy. It does not intend to ship significant protocol upgrades unless there is an urgent security issue or overwhelming community support, and the company intends to deprecate the Technical Collective over time.

Anyone can propose a protocol change by submitting a Quantus Improvement Proposal (QIP) for public review and discussing it at [research.quantus.com](https://research.quantus.com).

## 07 Roadmap

The current roadmap through 2026, subject to change.

Heisenberg Inception December 2024

Funding Secured, Substrate Chosen.

Resonance Alpha July 2025

Public Testnet, Dilithium Signatures.

Schrödinger Beta October 2025

Features Complete, Ready for Audit.

Dirac Beta November 2025

PoW changed to Poseidon2, Audits Addressed.

Planck Beta April 2026

Advanced Accounts, Multisigs, Hardware Wallet, Encrypted Transactions, Two-Layer ZK Aggregation.

Mainnet September 9, 2026

Mainnet Genesis.

  

## 08 Risks

Building Quantus comes with inherent risks.

### Implementation Issues

Flaws in software logic can cause serious failures in even the best designed systems. Quantus reduces this risk through independent audits by Neodyme, Eiger, and Hashcloak, a public Immunefi audit competition, formal verification of its ZK circuits and part of Plonky2, and continuous AI-assisted internal review.

No process eliminates implementation risk entirely.

#### Audits

SEGMENT

AUDITOR

DATE

Proof-of-Work and Poseidon2

Eiger (Equilibrium Group)

October 2025

ML-DSA signatures and HD wallet

Neodyme

December 2025

Wormhole ZK circuits

Eiger (Equilibrium Group)

March 2026

Substrate runtime and node

Eiger (Equilibrium Group)

May 2026

Wormhole circuit formal verification

Quantus, in the Lean proof assistant

June 2026

Threshold ML-DSA signatures

Hashcloak

2026

Whole chain, public audit competition

Immunefi

August 2026

Proof-of-Work and Poseidon2

AUDITOR Eiger (Equilibrium Group)

DATE October 2025

ML-DSA signatures and HD wallet

AUDITOR Neodyme

DATE December 2025

Wormhole ZK circuits

AUDITOR Eiger (Equilibrium Group)

DATE March 2026

Substrate runtime and node

AUDITOR Eiger (Equilibrium Group)

DATE May 2026

Wormhole circuit formal verification

AUDITOR Quantus, in the Lean proof assistant

DATE June 2026

Threshold ML-DSA signatures

AUDITOR Hashcloak

DATE 2026

Whole chain, public audit competition

AUDITOR Immunefi

DATE August 2026

Reports:

*   [Proof-of-Work and Poseidon2: report](https://github.com/Quantus-Network/qp-poseidon/blob/main/audits/Proof-of-Work%20and%20Poseidon%20Security%20Review%201.1.pdf)
*   [ML-DSA signatures and HD wallet: report](https://github.com/Quantus-Network/qp-rusty-crystals/blob/master/audits/Neodyme-Audit.pdf)
*   [Wormhole ZK circuits: report](https://github.com/Quantus-Network/qp-zk-circuits/blob/main/audits/EigerWormholeAudit.pdf)
*   [Substrate runtime and node: report](https://github.com/Quantus-Network/chain/blob/main/audits/quantus-substrate-audit-20260513.pdf)
*   [Wormhole circuit formal verification: specification](https://github.com/Quantus-Network/qp-zk-circuits/tree/main/formal)
*   [Whole chain, public audit competition: campaign](https://immunefi.com/bounty/audit-comp-quantus)

### NIST Algorithm Selection Issues

Flaws or backdoors in the selected post-quantum standards (e.g., ML-DSA, ML-KEM) could emerge after standardization. In the worst case, such flaws would allow an attacker to forge signatures by deriving a private key from the public, representing a catastrophic failure mode of the chain. If such flaws were made public, Quantus could be upgraded to a new algorithm.

### Quantum Computing Timelines

Quantum breakthroughs might arrive much later than anticipated, delaying the need for PQC; conversely, secretive development (e.g. by governments) could lead to sudden threats if the blockchain community fails to update swiftly.

### Other Considerations

General adoption barriers, regulatory uncertainties in finance/blockchain, and the inherent volatility of crypto ecosystems.

## 09 References & Further Reading

  

\[1\]

Shor, P. W. (1997). Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer. SIAM Journal on Computing, 26(5), 1484–1509. [https://doi.org/10.1137/S0097539795293172](https://doi.org/10.1137/S0097539795293172)

\[2\]

Grover, L.K. (1996). A fast quantum mechanical algorithm for database search. Proceedings of the Twenty-Eight Annual ACM Symposium on Theory of Computing, 212-219. [https://doi.org/10.1145/237814.237866](https://doi.org/10.1145/237814.237866)

\[3\]

Chainalysis. (2020, June). 60% of Bitcoin Is Held Long Term as Digital Gold. What About the Rest? Chainalysis Market Intel. Archived at [https://web.archive.org/web/20200622014856/https://blog.chainalysis.com/reports/bitcoin-market-data-exchanges-trading](https://web.archive.org/web/20200622014856/https://blog.chainalysis.com/reports/bitcoin-market-data-exchanges-trading)

\[4\]

National Institute of Standards and Technology. (2024). FIPS 204: Module-Lattice-Based Digital Signature Standard (ML-DSA). U.S. Department of Commerce. [https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)

\[5\]

National Institute of Standards and Technology. (2024). FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM). U.S. Department of Commerce. [https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)

\[6\]

Häner, T., Jaques, S., Naehrig, M., Roetteler, M., & Soeken, M. (2020). Improved quantum circuits for elliptic curve discrete logarithms. arXiv:2002.12480. [https://arxiv.org/abs/2002.12480](https://arxiv.org/abs/2002.12480)

\[7\]

Gidney, C., & Ekerå, M. (2021). How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits. arXiv:1905.09749. [https://arxiv.org/abs/1905.09749](https://arxiv.org/abs/1905.09749)

\[8\]

Aggarwal, D., et al. (2021). Assessment of Quantum Threat To Bitcoin and Derived Cryptocurrencies. ePrint IACR. [https://eprint.iacr.org/2021/967.pdf](https://eprint.iacr.org/2021/967.pdf)

\[9\]

Roetteler, M., Naehrig, M., Svore, K. M., & Lauter, K. (2017). Quantum resource estimates for computing elliptic curve discrete logarithms. arXiv:1706.06752. [https://arxiv.org/abs/1706.06752](https://arxiv.org/abs/1706.06752)

\[10\]

Open Quantum Safe Project. (n.d.). ML-DSA | Open Quantum Safe. Retrieved January 29, 2026, from [https://openquantumsafe.org/liboqs/algorithms/sig/ml-dsa.html](https://openquantumsafe.org/liboqs/algorithms/sig/ml-dsa.html)

\[11\]

Babbush, R., Zalcman, A., Gidney, C., Broughton, M., Khattar, T., Neven, H., Bergamaschi, T., Drake, J., & Boneh, D. (2026). Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations. Google Quantum AI. [https://quantumai.google/static/site-assets/downloads/cryptocurrency-whitepaper.pdf](https://quantumai.google/static/site-assets/downloads/cryptocurrency-whitepaper.pdf)

\[12\]

National Institute of Standards and Technology. (2024). NIST IR 8547: Transition to Post-Quantum Cryptography Standards. [https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf](https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf)

\[13\]

Executive Order 14412 of June 22, 2026, Securing the Nation Against Advanced Cryptographic Attacks, 91 Fed. Reg. 38483 (June 25, 2026). [https://www.federalregister.gov/d/2026-12909](https://www.federalregister.gov/d/2026-12909)

\[14\]

Signal. (2023, September 19). The PQXDH Key Agreement Protocol. [https://signal.org/blog/pqxdh/](https://signal.org/blog/pqxdh/)

\[15\]

Apple Security Engineering and Architecture. (2024, February 21). iMessage with PQ3: The new state of the art in quantum-secure messaging at scale. [https://security.apple.com/blog/imessage-pq3/](https://security.apple.com/blog/imessage-pq3/)

\[16\]

Cloudflare. (2025). The state of the post-quantum Internet in 2025. [https://blog.cloudflare.com/pq-2025/](https://blog.cloudflare.com/pq-2025/)

\[17\]

Blockchain.com. (2026). Bitcoin UTXO count. Retrieved September 3, 2026, from [https://www.blockchain.com/explorer/charts/utxo-count](https://www.blockchain.com/explorer/charts/utxo-count)

\[18\]

transactionfee.info. (n.d.). Payments spending SegWit. [https://transactionfee.info/charts/payments-spending-segwit/](https://transactionfee.info/charts/payments-spending-segwit/)

\[19\]

CoinDesk. (2026, July 4). Bitcoin experts split over plan to freeze Satoshi’s 1.1 million Bitcoin as quantum threat grows. [https://www.coindesk.com/business/2026/07/04/bitcoin-experts-split-over-plan-to-freeze-satoshi-s-1-1-million-bitcoin-as-quantum-threat-grows](https://www.coindesk.com/business/2026/07/04/bitcoin-experts-split-over-plan-to-freeze-satoshi-s-1-1-million-bitcoin-as-quantum-threat-grows)

\[20\]

Eigen Labs. (2026). ECDSA.fail: can you break ECDSA? [https://ecdsa.fail](https://ecdsa.fail)

### Further Reading

*   [Quantus Improvement Proposals (QIPs)](https://github.com/Quantus-Network/improvement-proposals)
*   [Documentation](https://docs.quantus.com)
*   [Research forum](https://research.quantus.com)
*   [The State of Quantum report](https://report.quantus.com)
*   [Source code](https://github.com/Quantus-Network)

On this page

*   [Legal Disclaimer](#legal-disclaimer)
*   [Contents](#contents)
*   [Introduction](#chapter-01)
*   [The Quantum Threat](#the-quantum-threat)
*   [Unique Value Proposition](#unique-value-proposition)
*   [The Quantum Threat to Blockchain](#chapter-02)
*   [Quantum Computing Basics](#quantum-computing-basics)
*   [The Shrinking Timeline](#the-shrinking-timeline)
*   [Four Threat Categories](#four-threat-categories)
*   [Scaling Challenges in Post-Quantum Cryptography](#scaling-challenges-in-post-quantum-cryptography)
*   [TPS vs QTPS](#tps-vs-qtps)
*   [The Migration Crisis](#chapter-03)
*   [The Coordination Problem](#the-coordination-problem)
*   [The Migration Timeline Problem](#the-migration-timeline-problem)
*   [The Lost Coin Problem](#the-lost-coin-problem)
*   [Quantus Architecture](#chapter-04)
*   [Foundation](#foundation)
*   [Quantum Secure](#quantum-secure)
*   [Private](#private)
*   [Scalable](#scalable)
*   [Money](#money)
*   [Account Security](#chapter-05)
*   [HD-Lattice](#hd-lattice)
*   [Check-Phrases](#check-phrases)
*   [Multisig Accounts](#multisig-accounts)
*   [Advanced Accounts](#advanced-accounts)
*   [Tokenomics and Governance](#chapter-06)
*   [Block Rewards](#block-rewards)
*   [Investor and Team Allocation](#investor-and-team-allocation)
*   [Company Allocation](#company-allocation)
*   [Transaction Fees](#transaction-fees)
*   [Network Upgrades](#network-upgrades)
*   [Governance System](#governance-system)
*   [Roadmap](#chapter-07)
*   [Risks](#chapter-08)
*   [Implementation Issues](#implementation-issues)
*   [NIST Algorithm Selection Issues](#nist-algorithm-selection-issues)
*   [Quantum Computing Timelines](#quantum-computing-timelines)
*   [Other Considerations](#other-considerations)
*   [References & Further Reading](#chapter-09)
*   [Further Reading](#further-reading)

[Back to top](#top)

## Changelog

*   Tokenomics: genesis pre-mint 27% (23% investors, founders, and team; 4% company), 73% mined.
*   Privacy Properties: state the concrete privacy model of encrypted sends.

[Quantus](/)

🇺🇸 English

*   [🇺🇸 English](/whitepaper/v0.4.1/)
*   [🇨🇳 中文](/zh-CN/whitepaper/v0.4.1/)
*   [🇰🇷 한국어](/ko-KR/whitepaper/v0.4.1/)
*   [🇮🇩 Bahasa Indonesia](/id-ID/whitepaper/v0.4.1/)
*   [🇯🇵 日本語](/ja-JP/whitepaper/v0.4.1/)
*   [🇷🇺 Русский](/ru-RU/whitepaper/v0.4.1/)
*   [🇪🇸 Español](/es-ES/whitepaper/v0.4.1/)
*   [🇩🇪 Deutsch](/de-DE/whitepaper/v0.4.1/)
*   [🇮🇳 हिन्दी](/hi-IN/whitepaper/v0.4.1/)

© 2026 Quantus. All rights reserved.

Protocol [Whitepaper](/whitepaper) [Technology](/technology) [Network](https://explorer.quantus.com/) [Wallet](/wallet) [Research](https://research.quantus.com/) [Documentation](https://docs.quantus.com/) [GitHub](https://github.com/Quantus-Network)

Community [Telegram](https://t.me/quantusnetwork) [X (Twitter)](https://x.com/QuantusNetwork) [Instagram](https://www.instagram.com/quantusnetwork/) [YouTube](https://www.youtube.com/@QuantusNetwork)

Company [Blog](/blog) [QDay Podcast](/community) [Contact](/community#contact) [Privacy Policy](/privacy-policy) [Terms of Service](/terms) [CoinGecko](https://www.coingecko.com/en/coins/quantus) [Blockspot.io](https://blockspot.io/coin/quantus/)