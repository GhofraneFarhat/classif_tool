import re
from collections import defaultdict

def classify_contigs(input_fasta):
    """
    Classify contigs from a FASTA file as chromosomes, plasmids, or ambiguous, and write the results to a new FASTA file.
    
    Args:
        input_fasta (str): Path to the input FASTA file.
    """
    output_fasta = "class.fasta"
    classifications = defaultdict(str)
    
    with open(input_fasta, 'r') as file:
        for line in file:
            if line.startswith('>'):
                contig_name = line.strip('>\n')
                
                # Check if the contig name contains 'chromosome' or 'plasmid'
                if 'chromosome' in contig_name.lower():
                    classifications[contig_name] = 'chromosome'
                elif 'plasmid' in contig_name.lower():
                    classifications[contig_name] = 'plasmid'
                else:
                    classifications[contig_name] = 'ambiguous'
    
    with open(output_fasta, 'w') as output_file:
        for contig, classification in classifications.items():
            output_file.write(f'>{contig} ({classification})\n')
            
            # Write the sequence for the contig
            with open(input_fasta, 'r') as input_file:
                found_contig = False
                for seq_line in input_file:
                    if seq_line.startswith(f'>{contig}'):
                        found_contig = True
                    elif found_contig and not seq_line.startswith('>'):
                        output_file.write(seq_line)
                    elif found_contig and seq_line.startswith('>'):
                        break
    
    return output_fasta

# Example usage
input_fasta = "inputclass.fasta"
output_fasta = classify_contigs(input_fasta)
print(f'Results written to {output_fasta}')