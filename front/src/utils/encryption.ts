/**
 * Encryption Utility using Web Crypto API
 * Implements E2EE with AES-GCM and PBKDF2 for key derivation.
 */

const ITERATIONS = 100000;
const KEY_LEN = 256;
const ALGO = 'AES-GCM';

/**
 * Derive an encryption key from a master password and salt.
 */
async function deriveKey(password: string, salt: string): Promise<CryptoKey> {
    const encoder = new TextEncoder();
    const passwordData = encoder.encode(password);
    const saltData = encoder.encode(salt);

    const baseKey = await crypto.subtle.importKey(
        'raw',
        passwordData,
        'PBKDF2',
        false,
        ['deriveKey']
    );

    return crypto.subtle.deriveKey(
        {
            name: 'PBKDF2',
            salt: saltData,
            iterations: ITERATIONS,
            hash: 'SHA-256',
        },
        baseKey,
        { name: ALGO, length: KEY_LEN },
        false,
        ['encrypt', 'decrypt']
    );
}

/**
 * Encrypt a string using a master password.
 */
export async function encryptData(data: string, password: string, salt: string): Promise<string> {
    const encoder = new TextEncoder();
    const key = await deriveKey(password, salt);
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const encodedData = encoder.encode(data);

    const encrypted = await crypto.subtle.encrypt(
        { name: ALGO, iv },
        key,
        encodedData
    );

    // Combine IV and encrypted data into a single hex string
    const combined = new Uint8Array(iv.length + encrypted.byteLength);
    combined.set(iv);
    combined.set(new Uint8Array(encrypted), iv.length);

    return btoa(String.fromCharCode(...combined));
}

/**
 * Decrypt a base64 string using a master password.
 */
export async function decryptData(encryptedBase64: string, password: string, salt: string): Promise<string> {
    const decoder = new TextDecoder();
    const combined = new Uint8Array(
        atob(encryptedBase64)
            .split('')
            .map((c) => c.charCodeAt(0))
    );

    const iv = combined.slice(0, 12);
    const data = combined.slice(12);
    const key = await deriveKey(password, salt);

    try {
        const decrypted = await crypto.subtle.decrypt(
            { name: ALGO, iv },
            key,
            data
        );

        return decoder.decode(decrypted);
    } catch (e) {
        throw new Error('Decryption failed. Check your master password.');
    }
}
