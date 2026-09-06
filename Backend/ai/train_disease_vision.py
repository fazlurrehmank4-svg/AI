"""
Plant Disease Computer Vision AI Training Pipeline (PyTorch)
Trains a Deep Convolutional Network on Data/Train/archive (1) across 9 plant species
and 27 distinct disease and healthy states.
"""

import os
import json
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
from typing import List, Tuple, Dict, Any

# Standard Crop Disease Treatment and Curative Guide Mapping
DISEASE_REMEDY_GUIDE = {
    "Apple___Apple_Scab": {
        "disease_name": "Apple Scab (Venturia inaequalis)",
        "crop": "Apple",
        "severity": "High",
        "symptoms": "Velvety brown or olive-green spots on leaves and scabby lesions on fruits.",
        "causes": "High humidity, prolonged leaf wetness in spring, and airborne fungal spores.",
        "precautions": [
            "Rake and destroy fallen infected leaves during winter dormancy.",
            "Apply protective fungicide (captan, mancozeb, or myclobutanil) starting at green-tip bud break.",
            "Prune canopy branches to accelerate foliage drying after rain."
        ]
    },
    "Apple___Black_Rot": {
        "disease_name": "Black Rot (Botryosphaeria obtusa)",
        "crop": "Apple",
        "severity": "High",
        "symptoms": "Frog-eye leaf spots, limb cankers, and mummified rotting black apples.",
        "causes": "Fungal spores entering through branch wounds or insect damage during warm rains.",
        "precautions": [
            "Prune out dead wood, cankers, and mummified fruits from previous seasons.",
            "Apply protective fungicides from petal fall through harvest.",
            "Control codling moth and curculio insects that create entry wounds."
        ]
    },
    "Apple___Cedar_Apple_Rust": {
        "disease_name": "Cedar Apple Rust (Gymnosporangium juniperi-virginianae)",
        "crop": "Apple",
        "severity": "Moderate",
        "symptoms": "Bright yellow-orange spots on upper leaf surfaces and tubular spore cups underneath.",
        "causes": "Fungus cycling between eastern red cedar trees and apple orchards during moist spring periods.",
        "precautions": [
            "Remove surrounding cedar/juniper galls within 1-2 miles of the orchard if feasible.",
            "Apply sterol inhibitor fungicides (myclobutanil) between pink bud and petal fall.",
            "Plant rust-resistant apple cultivars like Enterprise or Liberty."
        ]
    },
    "Apple___Healthy": {
        "disease_name": "Healthy Apple Canopy",
        "crop": "Apple",
        "severity": "None",
        "symptoms": "Vibrant green leaves with no visible lesions or necrotic tissue.",
        "causes": "Balanced nutrition and optimal orchard management.",
        "precautions": [
            "Maintain scheduled preventative scouting and balanced foliar nutrition.",
            "Ensure regular irrigation and seasonal pruning."
        ]
    },
    "Cherry___Powdery_Mildew": {
        "disease_name": "Cherry Powdery Mildew (Podosphaera clandestina)",
        "crop": "Cherry",
        "severity": "Moderate",
        "symptoms": "White powdery fungal patches on young leaves, curled margins, and unmarketable fruit.",
        "causes": "Warm days followed by humid nights in shaded canopy microclimates.",
        "precautions": [
            "Prune interior branches to enhance light penetration and air movement.",
            "Apply sulfur-based or potassium bicarbonate fungicides at first sign.",
            "Avoid excessive late-season nitrogen applications."
        ]
    },
    "Cherry___Healthy": {
        "disease_name": "Healthy Cherry Canopy",
        "crop": "Cherry",
        "severity": "None",
        "symptoms": "Uniform leaf color and intact cuticle layer.",
        "causes": "Optimal environmental conditions.",
        "precautions": [
            "Maintain routine orchard scouting and regulated deficit watering."
        ]
    },
    "Corn___Common_Rust": {
        "disease_name": "Corn Common Rust (Puccinia sorghi)",
        "crop": "Corn",
        "severity": "Moderate",
        "symptoms": "Oval to elongated cinnamon-brown pustules on both leaf surfaces.",
        "causes": "Wind-blown urediniospores from warm southern zones combined with high humidity.",
        "precautions": [
            "Select resistant maize hybrids.",
            "Apply foliar triazole/strobilurin fungicides if rust reaches ear leaf prior to silking.",
            "Scout weekly during late vegetative stages."
        ]
    },
    "Corn___Gray_Leaf_Spot": {
        "disease_name": "Gray Leaf Spot (Cercospora zeae-maydis)",
        "crop": "Corn",
        "severity": "High",
        "symptoms": "Rectangular, brown to gray necrotic lesions running parallel to leaf veins.",
        "causes": "Continuous corn cropping, minimal tillage residue, and warm humid weather (>85% RH).",
        "precautions": [
            "Practice crop rotation with soybeans or legumes.",
            "Till under or shred infected crop residue to accelerate breakdown.",
            "Apply preventative foliar fungicide at VT-R1 growth stages."
        ]
    },
    "Corn___Northern_Leaf_Blight": {
        "disease_name": "Northern Corn Leaf Blight (Exserohilum turcicum)",
        "crop": "Corn",
        "severity": "High",
        "symptoms": "Large, cigar-shaped grayish-green to tan lesions (1-6 inches long) on leaves.",
        "causes": "Moderate temperatures (18-27C) with heavy dews and high humidity.",
        "precautions": [
            "Plant resistant corn hybrids with Ht gene resistance.",
            "Rotate crops and avoid continuous corn fields.",
            "Apply strobilurin/triazole fungicide if lesions appear on third leaf below whorl."
        ]
    },
    "Corn___Healthy": {
        "disease_name": "Healthy Corn Foliage",
        "crop": "Corn",
        "severity": "None",
        "symptoms": "Vigorous green leaves with strong stalk strength and no fungal pustules.",
        "causes": "Adequate soil nitrogen and optimal climate conditions.",
        "precautions": [
            "Maintain side-dress nitrogen schedule and monitor soil moisture at tasseling."
        ]
    },
    "Grape___Black_Rot": {
        "disease_name": "Grape Black Rot (Guignardia bidwellii)",
        "crop": "Grape",
        "severity": "High",
        "symptoms": "Reddish-brown circular spots with dark borders on leaves; berries shrivel into hard black mummies.",
        "causes": "Overwintering fungal pycnidia on mummified berries splashing onto new spring shoots.",
        "precautions": [
            "Remove all mummified berries and pruned canes during winter dormant cleanup.",
            "Apply protective fungicide (mancozeb, captan, or tebuconazole) starting at 1-inch shoot growth.",
            "Maintain open canopy trellis training."
        ]
    },
    "Grape___Esca": {
        "disease_name": "Grape Esca / Black Measles",
        "crop": "Grape",
        "severity": "High",
        "symptoms": "Tiger-stripe chlorotic patterns between leaf veins and dark purple speckles on berry skin.",
        "causes": "Complex of trunk-inhabiting wood rot fungi entering through pruning wounds.",
        "precautions": [
            "Disinfect pruning shears regularly with 70% ethanol.",
            "Apply pruning wound sealants immediately after winter cane cuts.",
            "Avoid aggressive pruning during rainy spells."
        ]
    },
    "Grape___Leaf_Blight": {
        "disease_name": "Grape Leaf Blight (Pseudocercospora vitis)",
        "crop": "Grape",
        "severity": "Moderate",
        "symptoms": "Irregular dark brown patches on older foliage, premature defoliation in late summer.",
        "causes": "Dense unmanaged foliage and humid air stagnation under the trellis.",
        "precautions": [
            "Perform leaf-pulling around grape clusters to maximize air movement.",
            "Apply post-bloom copper sprays to protect leaves."
        ]
    },
    "Grape___Healthy": {
        "disease_name": "Healthy Grape Vine",
        "crop": "Grape",
        "severity": "None",
        "symptoms": "Lush canopy with no spotting or leaf scorch.",
        "causes": "Balanced trellis pruning and adequate nutrition.",
        "precautions": [
            "Maintain shoot positioning and drip irrigation schedule."
        ]
    },
    "Peach___Bacterial_Spot": {
        "disease_name": "Peach Bacterial Spot (Xanthomonas arboricola pv. pruni)",
        "crop": "Peach",
        "severity": "High",
        "symptoms": "Water-soaked angular leaf spots leading to shot-hole dropping, pitted and gumming fruit surfaces.",
        "causes": "Bacterial inoculum spread by wind-driven rains during warm spring storms.",
        "precautions": [
            "Plant windbreaks to reduce windblown grit and micro-wounds.",
            "Apply dormant copper sprays and oxytetracycline formulations during cover sprays.",
            "Select resistant cultivars."
        ]
    },
    "Peach___Healthy": {
        "disease_name": "Healthy Peach Tree Foliage",
        "crop": "Peach",
        "severity": "None",
        "symptoms": "Clean elongated leaves free of necrotic holes or bacterial oozing.",
        "causes": "Proper orchard aeration and balanced soil nutrition.",
        "precautions": [
            "Maintain open-center vase pruning and monitor for peach tree borers."
        ]
    },
    "Pepper___Bacterial_Spot": {
        "disease_name": "Pepper Bacterial Spot (Xanthomonas euvesicatoria)",
        "crop": "Pepper",
        "severity": "High",
        "symptoms": "Small, water-soaked dark spots on leaves with yellow haloes, defoliation, and fruit blistering.",
        "causes": "Overhead sprinkler irrigation, infected seeds, and temperatures between 24-32C with high RH.",
        "precautions": [
            "Use certified pathogen-free seeds and transplants.",
            "Avoid overhead irrigation; switch exclusively to drip lines.",
            "Apply preventative copper bactericide combined with mancozeb."
        ]
    },
    "Pepper___Healthy": {
        "disease_name": "Healthy Pepper Foliage",
        "crop": "Pepper",
        "severity": "None",
        "symptoms": "Glossy green leaves with intact structure.",
        "causes": "Good drainage and proper moisture control.",
        "precautions": [
            "Maintain regular calcium-potassium feeding and drip moisture."
        ]
    },
    "Potato___Early_Blight": {
        "disease_name": "Potato Early Blight (Alternaria solani)",
        "crop": "Potato",
        "severity": "Moderate",
        "symptoms": "Dark brown circular spots with concentric target-board rings on older lower leaves.",
        "causes": "Alternating wet and dry periods, plant stress during tuber bulk-filling.",
        "precautions": [
            "Maintain balanced nitrogen to prevent early vine senescence.",
            "Avoid late-afternoon overhead watering that leaves foliage wet overnight.",
            "Apply preventative chlorothalonil or azoxystrobin sprays."
        ]
    },
    "Potato___Late_Blight": {
        "disease_name": "Potato Late Blight (Phytophthora infestans)",
        "crop": "Potato",
        "severity": "Critical",
        "symptoms": "Rapidly expanding water-soaked black lesions with white sporulation on leaf undersides; rotting tubers.",
        "causes": "Cool, foggy, wet weather (12-22C) with high relative humidity (>90%).",
        "precautions": [
            "Earthing up soil ridges deeply to prevent spore washdown into tubers.",
            "Apply systemic fungicides (metalaxyl, dimethomorph, mandipropamid) immediately upon alert.",
            "Destroy cull piles and harvest only after vines have completely died down."
        ]
    },
    "Potato___Healthy": {
        "disease_name": "Healthy Potato Canopy",
        "crop": "Potato",
        "severity": "None",
        "symptoms": "Robust green haulm foliage without blighting or yellowing.",
        "causes": "Optimal soil moisture, hilling, and preventive scouting.",
        "precautions": [
            "Ensure regular hilling (earthing up) and stop watering 10 days before harvest."
        ]
    },
    "Strawberry___Leaf_Scorch": {
        "disease_name": "Strawberry Leaf Scorch (Diplocarpon earlianum)",
        "crop": "Strawberry",
        "severity": "Moderate",
        "symptoms": "Small purplish-red blotches coalescing to give leaves a scorched, burnt appearance.",
        "causes": "Prolonged leaf wetness from rain or overhead sprinklers in moderate temperatures.",
        "precautions": [
            "Plant in well-drained raised beds with plastic or straw mulch.",
            "Use drip irrigation under mulch.",
            "Remove and destroy severely affected leaves post-harvest."
        ]
    },
    "Strawberry___Healthy": {
        "disease_name": "Healthy Strawberry Canopy",
        "crop": "Strawberry",
        "severity": "None",
        "symptoms": "Vibrant trifoliate green leaves with no purple blotches.",
        "causes": "Clean planting stock and well-drained bed culture.",
        "precautions": [
            "Keep bed mulched and scout weekly for spider mites and crown rot."
        ]
    },
    "Tomato___Bacterial_Spot": {
        "disease_name": "Tomato Bacterial Spot (Xanthomonas)",
        "crop": "Tomato",
        "severity": "High",
        "symptoms": "Small dark brown spots with chlorotic yellow borders on leaves, scabby fruit specks.",
        "causes": "High humidity, rain splash, and warm temperatures (24-30C).",
        "precautions": [
            "Avoid working in field when plants are wet.",
            "Spray copper hydroxide mixed with mancozeb as protective measure.",
            "Stake and mulch plants to prevent soil splash."
        ]
    },
    "Tomato___Early_Blight": {
        "disease_name": "Tomato Early Blight (Alternaria solani)",
        "crop": "Tomato",
        "severity": "Moderate",
        "symptoms": "Concentric dark brown rings on lower leaves progressing upward; collar rot on stems.",
        "causes": "Warm humid conditions, dew formation, and spores residing in infected crop residue.",
        "precautions": [
            "Prune lower bottom branches 12 inches above soil line for aeration.",
            "Apply mulch around base and irrigate with drip lines.",
            "Rotate tomato plots every 2-3 years."
        ]
    },
    "Tomato___Late_Blight": {
        "disease_name": "Tomato Late Blight (Phytophthora infestans)",
        "crop": "Tomato",
        "severity": "Critical",
        "symptoms": "Large greasy grayish-brown leaf patches, white fluffy mold under humid mornings, rotting green fruits.",
        "causes": "Cool damp weather, prolonged leaf wetness, and windborne sporangia.",
        "precautions": [
            "Apply protective copper or systemic phosphonate fungicides before extended rain spells.",
            "Pull out and burn severely blighted whole plants to protect neighboring crops.",
            "Never use overhead sprinkler irrigation."
        ]
    },
    "Tomato___Healthy": {
        "disease_name": "Healthy Tomato Canopy",
        "crop": "Tomato",
        "severity": "None",
        "symptoms": "Uniform deep green foliage with sturdy indeterminate vines.",
        "causes": "Balanced N-P-K nutrition, drip irrigation, and staking.",
        "precautions": [
            "Maintain consistent drip watering to prevent blossom end rot and fruit splitting."
        ]
    }
}

class PlantDiseaseDataset(Dataset):
    """
    Scans nested crop/disease folders in archive (1)/train or archive (1)/valid
    """
    def __init__(self, root_dir: str, class_to_idx: Dict[str, int], transform=None, max_samples_per_class: int = 1200):
        self.samples: List[Tuple[str, int]] = []
        self.transform = transform
        self.class_to_idx = class_to_idx

        for plant in sorted(os.listdir(root_dir)):
            plant_path = os.path.join(root_dir, plant)
            if not os.path.isdir(plant_path):
                continue
            for disease in sorted(os.listdir(plant_path)):
                disease_path = os.path.join(plant_path, disease)
                if not os.path.isdir(disease_path):
                    continue
                
                # Normalize key: e.g. "Apple___Apple_Scab"
                class_key = f"{plant}___{disease.replace(' ', '_')}"
                if class_key not in self.class_to_idx:
                    continue
                
                idx = self.class_to_idx[class_key]
                img_files = [
                    os.path.join(disease_path, f)
                    for f in os.listdir(disease_path)
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
                ]
                # Balance dataset if large
                if max_samples_per_class and len(img_files) > max_samples_per_class:
                    img_files = img_files[:max_samples_per_class]

                for img_p in img_files:
                    self.samples.append((img_p, idx))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, target = self.samples[idx]
        try:
            with open(path, 'rb') as f:
                img = Image.open(f).convert('RGB')
        except Exception:
            # Fallback black image if file read error
            img = Image.new('RGB', (128, 128))

        if self.transform is not None:
            img = self.transform(img)

        return img, target

class CropDiseaseCNN(nn.Module):
    """
    High-Performance, lightweight Deep Residual CNN for Edge & Server Leaf Scan Inference.
    """
    def __init__(self, num_classes: int = 27):
        super(CropDiseaseCNN, self).__init__()
        
        # Block 1
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2) # -> 64x64
        )
        
        # Block 2
        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2) # -> 32x32
        )

        # Block 3
        self.conv3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2) # -> 16x16
        )

        # Block 4
        self.conv4 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2) # -> 8x8
        )

        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.classifier = nn.Sequential(
            nn.Dropout(0.35),
            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.20),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.global_pool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

def build_class_index_map(data_root: str) -> Dict[str, int]:
    classes = []
    for plant in sorted(os.listdir(data_root)):
        p_path = os.path.join(data_root, plant)
        if os.path.isdir(p_path):
            for disease in sorted(os.listdir(p_path)):
                d_path = os.path.join(p_path, disease)
                if os.path.isdir(d_path):
                    class_key = f"{plant}___{disease.replace(' ', '_')}"
                    if class_key not in classes:
                        classes.append(class_key)
    classes = sorted(classes)
    return {c: i for i, c in enumerate(classes)}

def train_disease_vision_model(
    data_dir: str = "Data/Train/archive (1)",
    save_model_path: str = "Backend/ai/saved_models/crop_disease_vision.pt",
    save_classes_path: str = "Backend/ai/saved_models/disease_classes.json",
    num_epochs: int = 4,
    batch_size: int = 64,
    learning_rate: float = 0.0015
):
    print("=" * 65, flush=True)
    print("       TRAINING PLANT DISEASE COMPUTER VISION AI MODEL", flush=True)
    print("=" * 65, flush=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Hardware] Using compute device: {device}", flush=True)

    train_dir = os.path.join(data_dir, "train")
    valid_dir = os.path.join(data_dir, "valid")

    if not os.path.exists(train_dir):
        raise FileNotFoundError(f"Train directory not found at {train_dir}")

    # Build and save class mapping
    class_to_idx = build_class_index_map(train_dir)
    idx_to_class = {v: k for k, v in class_to_idx.items()}
    num_classes = len(class_to_idx)
    print(f"[Dataset] Identified {num_classes} plant-disease classes across 9 crop species.", flush=True)

    # Data transforms
    train_transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.15, contrast=0.15),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    val_transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    print("[Dataset] Indexing image paths and constructing data batches...", flush=True)
    train_dataset = PlantDiseaseDataset(train_dir, class_to_idx, transform=train_transform, max_samples_per_class=150)
    val_dataset = PlantDiseaseDataset(valid_dir if os.path.exists(valid_dir) else train_dir, class_to_idx, transform=val_transform, max_samples_per_class=40)

    print(f"[Dataset] Loaded {len(train_dataset)} training images and {len(val_dataset)} validation images.", flush=True)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    # Initialize Model
    model = CropDiseaseCNN(num_classes=num_classes).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)

    best_val_acc = 0.0

    for epoch in range(1, num_epochs + 1):
        start_time = time.time()
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0

        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct_train += (preds == labels).sum().item()
            total_train += labels.size(0)

        scheduler.step()
        train_loss = running_loss / max(1, total_train)
        train_acc = (correct_train / max(1, total_train)) * 100.0

        # Evaluation on Validation set
        model.eval()
        val_loss = 0.0
        correct_val = 0
        total_val = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(device)
                labels = labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                correct_val += (preds == labels).sum().item()
                total_val += labels.size(0)

        val_loss = val_loss / max(1, total_val)
        val_acc = (correct_val / max(1, total_val)) * 100.0
        elapsed = time.time() - start_time

        print(f"Epoch [{epoch}/{num_epochs}] ({elapsed:.1f}s) - Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}% | Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%", flush=True)

        if val_acc > best_val_acc or epoch == num_epochs:
            best_val_acc = max(best_val_acc, val_acc)
            os.makedirs(os.path.dirname(save_model_path), exist_ok=True)
            torch.save({
                'model_state_dict': model.state_dict(),
                'num_classes': num_classes,
                'class_to_idx': class_to_idx,
                'val_accuracy': val_acc,
                'epoch': epoch,
                'timestamp': time.time()
            }, save_model_path)

    # Save rich disease metadata json
    metadata = {
        "classes": [
            {
                "index": idx,
                "class_id": class_key,
                "display_name": DISEASE_REMEDY_GUIDE.get(class_key, {}).get("disease_name", class_key.replace("___", " - ").replace("_", " ")),
                "crop": DISEASE_REMEDY_GUIDE.get(class_key, {}).get("crop", class_key.split("___")[0]),
                "severity": DISEASE_REMEDY_GUIDE.get(class_key, {}).get("severity", "Moderate"),
                "symptoms": DISEASE_REMEDY_GUIDE.get(class_key, {}).get("symptoms", "Foliar discoloration observed."),
                "causes": DISEASE_REMEDY_GUIDE.get(class_key, {}).get("causes", "Environmental factors and fungal/bacterial vectors."),
                "precautions": DISEASE_REMEDY_GUIDE.get(class_key, {}).get("precautions", ["Isolate affected leaves and maintain good soil drainage."])
            }
            for class_key, idx in sorted(class_to_idx.items(), key=lambda x: x[1])
        ],
        "metrics": {
            "best_validation_accuracy": float(best_val_acc),
            "num_classes": num_classes,
            "trained_samples": len(train_dataset)
        }
    }

    with open(save_classes_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n[Complete] Vision Model saved to {save_model_path}", flush=True)
    print(f"[Complete] Metadata saved to {save_classes_path}", flush=True)
    print(f"[Summary] Best Validation Accuracy: {best_val_acc:.2f}%", flush=True)

if __name__ == "__main__":
    train_disease_vision_model()
