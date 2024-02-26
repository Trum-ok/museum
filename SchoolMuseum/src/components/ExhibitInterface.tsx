export interface Exhibit {
    id: number;
    name: string;
    quantity: number;
    obtaining: string;
    discovery: string;
    description: string;
    assignment: string;
    image: string
    inventory_number: {
        number: number;
        collection: string;
        fund: string;
    };
    visible: boolean;
}
